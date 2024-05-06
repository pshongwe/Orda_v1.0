import os
import uuid
import logging
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_restx import Api, Resource, fields, Namespace


app = Flask(__name__)

# Retrieve environment variables
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME')

# Construct the MongoDB URI
app.config["MONGO_URI"] = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DBNAME}?retryWrites=true&w=majority"

mongo = PyMongo(app)
CORS(app)
# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
api = Api(app, version='1.0', title='OrdaSys API', description='OrdaSys API Documentation', doc='/swagger/')

# Namespaces
ns_customers = Namespace('customers', description='Customer operations')
ns_items = Namespace('items', description='Item operations')
ns_orders = Namespace('orders', description='Order operations')

# add namespaces
api.add_namespace(ns_customers)
api.add_namespace(ns_items)
api.add_namespace(ns_orders)

# Model definitions
get_model = api.model('Order', {
    'order_id': fields.String(description='The order unique identifier', readonly=True),
    'customer_id': fields.String(description='Customer identifier'),
    'items': fields.List(fields.Nested(api.model('Item', {
        'item_id': fields.String(required=True, description='Item identifier'),
        'quantity': fields.Integer(required=True, description='Quantity of the item'),
        'price': fields.Float(required=True, description='Price of the item')
    })), required=True, description='List of items'),
    'total': fields.Float(required=True, description='Total price of the order'),
    'date': fields.String(required=True, description='Date of the order'),
    'status': fields.String(required=True, description='Status of the order')
})

post_model = api.model('Order', {
    'order_id': fields.String(required=True, description='The order unique identifier'),
    'customer_id': fields.String(required=True, description='Customer identifier'),
    'items': fields.List(fields.Nested(api.model('Item', {
        'item_id': fields.String(required=True, description='Item identifier'),
        'quantity': fields.Integer(required=True, description='Quantity of the item'),
        'price': fields.Float(required=True, description='Price of the item')
    })), required=True, description='List of items'),
    'total': fields.Float(required=True, description='Total price of the order'),
    'date': fields.String(required=True, description='Date of the order'),
    'status': fields.String(required=True, description='Status of the order')
})

order_model = api.model('Order', {
    'order_id': fields.String(description='The order unique identifier', required=True),
    'customer_id': fields.String(description='Customer identifier', required=True),
    'items': fields.List(fields.Nested(api.model('Item', {
        'item_id': fields.String(required=True, description='Item identifier'),
        'quantity': fields.Integer(required=True, description='Quantity of the item'),
        'price': fields.Float(required=True, description='Price of the item')
    })), required=True, description='List of items'),
    'total': fields.Float(required=True, description='Total price of the order'),
    'date': fields.String(required=True, description='Date of the order'),
    'status': fields.String(required=True, description='Status of the order')
})

customer_model = api.model('Customer', {
    'customer_id': fields.String(required=True, description='The unique identifier for the customer'),
    'name': fields.String(required=True, description='Full name of the customer'),
    'email': fields.String(required=True, description='Email address of the customer'),
    'password': fields.String(required=True, description='Password for the customer account'),
    'address': fields.String(required=True, description='Physical address of the customer')
})

item_model = api.model('Item', {
    'item_id': fields.String(required=True, description='The unique identifier for the item'),
    'name': fields.String(required=True, description='Item name'),
    'price': fields.Float(required=True, description='Item price'),
    'stock': fields.Integer(required=True, description='Item stock count')
})

@ns_orders.route('/api/v1/orders')
class OrderList(Resource):
    @api.doc('list_orders')
    @api.marshal_list_with(get_model)
    def get(self):
        '''List all orders'''
        orders = mongo.db.orders.find()
        return list(orders)

    @api.doc('create_order')
    @api.expect(post_model)
    @api.marshal_with(get_model, code=201)  # Ensure this uses a model that includes the order_id
    def post(self):
        '''Create a new order'''
        data = api.payload
        if not data:
            api.abort(400, "No data provided")

        # Generate a unique order_id
        order_id = str(uuid.uuid4())

        # Insert the order into the database with the generated order_id
        order = {
            'order_id': order_id,
            **data
        }
        mongo.db.orders.insert_one(order)
        new_order = mongo.db.orders.find_one({'order_id': order_id})

        return new_order, 201


@ns_orders.route('/api/v1/orders/<string:order_id>')
class Order(Resource):
    @api.doc('get_order')
    @api.marshal_with(order_model)
    def get(self, order_id):
        '''Get details of a specific order'''
        order = mongo.db.orders.find_one({'order_id': order_id})
        if not order:
            return {'message': 'Order not found'}, 404
        return order

    @api.doc('update_order')
    @api.expect(order_model)
    @api.marshal_with(order_model)
    def put(self, order_id):
        '''Update details of a specific order'''
        data = api.payload
        if not data:
            return {'message': 'No data provided'}, 400

        # Update the order in the database
        updated_order = mongo.db.orders.find_one_and_update(
            {'order_id': order_id},
            {'$set': data},
            return_document=True
        )
        if not updated_order:
            return {'message': 'Order not found'}, 404
        return updated_order

    @api.doc('delete_order')
    def delete(self, order_id):
        '''Delete a specific order'''
        result = mongo.db.orders.delete_one({'order_id': order_id})
        if result.deleted_count == 0:
            return {'message': 'Order not found'}, 404
        return {'message': 'Order deleted successfully'}


@ns_orders.route('/api/v1/orders/<string:order_id>/status')
class OrderStatus(Resource):
    @api.doc('get_order_status')
    def get(self, order_id):
        '''Get the current status of a specific order'''
        order = mongo.db.orders.find_one({'order_id': order_id})
        if not order:
            return {'message': 'Order not found'}, 404
        return {'status': order['status']}

    @api.doc('update_order_status')
    @api.expect(api.model('StatusUpdate', {
        'status': fields.String(required=True, description='New status of the order')
    }))
    def put(self, order_id):
        '''Upadate the status of a specific order'''
        data = api.payload
        if not data:
            return {'message': 'No data provided'}, 400

        # Update the status of the order in the database
        updated_order = mongo.db.orders.find_one_and_update(
            {'order_id': order_id},
            {'$set': {'status': data['status']}},
            return_document=True
        )
        if not updated_order:
            return {'message': 'Order not found'}, 404
        return updated_order


@ns_customers.route('/api/v1/customers')
class CustomerList(Resource):
    @api.doc('list_customers')
    @api.marshal_list_with(customer_model)
    def get(self):
        '''List all customers'''
        customers = mongo.db.customers.find({}, {'password': 0})  # Exclude passwords from the query result
        return list(customers)

    @api.doc('register_customer')
    @api.expect(customer_model)
    @api.marshal_with(customer_model, code=201)
    def post(self):
        '''Register a new customer'''
        data = api.payload
        if not data:
            api.abort(400, "No data provided")

        # Hash the password before storing it
        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(data['password'])

        customer = {
            'customer_id': str(uuid.uuid4()),  # Generate a new UUID for the customer
            'name': data['name'],
            'email': data['email'],
            'password': hashed_password,
            'address': data['address']
        }
        mongo.db.customers.insert_one(customer)
        del customer['password']  # Remove password from response for security
        return customer, 201


@ns_customers.route('/api/v1/customers/<string:customer_id>')
class Customer(Resource):
    @api.doc('get_customer')
    @api.marshal_with(customer_model)
    def get(self, customer_id):
        '''Retrieve a specific customer by their customer ID'''
        customer = mongo.db.customers.find_one({'customer_id': customer_id})
        if not customer:
            return {'message': 'Customer not found'}, 404
        del customer['password']  # Remove password from response for security
        return customer
    
    @api.doc('update_customer')
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        '''Update details of a specific customer'''
        data = api.payload
        if not data:
            return {'message': 'No data provided'}, 400

        # Update the customer in the database
        updated_customer = mongo.db.customers.find_one_and_update(
            {'customer_id': customer_id},
            {'$set': data},
            return_document=True
        )
        if not updated_customer:
            return {'message': 'Customer not found'}, 404
        del updated_customer['password']  # Remove password from response for security
        return updated_customer
    
    @api.doc('delete_customer')
    def delete(self, customer_id):
        '''Delete a specific customer'''
        result = mongo.db.customers.delete_one({'customer_id': customer_id})
        if result.deleted_count == 0:
            return {'message': 'Customer not found'}, 404
        return {'message': 'Customer deleted successfully'}
    
@ns_items.route('/api/v1/items')
class itemsList(Resource):
    @api.doc('get_items')
    @api.marshal_list_with(item_model)
    def get(self):
        '''Retrieve all items'''
        items = mongo.db.items.find()
        return list(items), 200
    
    @api.doc('add_item')
    @api.expect(item_model)
    @api.marshal_with(item_model, code=201)
    def post(self):
        '''Add a new item'''
        item = api.payload
        item['item_id'] = str(uuid.uuid4())  # Generate a new UUID for the item
        mongo.db.items.insert_one(item)  # Insert the new item into the database
        return item, 201
    
@ns_items.route('/api/v1/items/<string:item_id>')
class Item(Resource):
    @api.doc('get_item')
    @api.marshal_with(item_model)
    def get(self, item_id):
        '''Retrieve a specific item by its item ID'''
        item = mongo.db.items.find_one({'item_id': item_id})
        if item:
            return item, 200
        else:
            return {'message': 'Item not found'}, 404
        
    @api.doc('update_item')
    @api.expect(item_model)
    @api.marshal_with(item_model)
    def put(self, item_id):
        '''Update an existing item with new data'''
        updated_item = api.payload
        mongo.db.items.update_one({'item_id': item_id}, {'$set': updated_item })
        return updated_item, 200
    
    @api.doc('delete_item')
    @api.response(204, 'Item deleted')
    def delete(self, item_id):
        '''Delete an item by item ID'''
        mongo.db.items.delete_one({'item_id': item_id})
        return '', 204


if __name__ == '__main__':
    app.run(debug=True, port=5000)