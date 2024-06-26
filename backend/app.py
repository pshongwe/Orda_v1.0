import os
import uuid
import logging
from functools import wraps
from flask import Flask, request, jsonify
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from flask_restx import Api, Resource, fields, Namespace
from bson import ObjectId

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
app.config['DEBUG'] = True

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
ns_customers = Namespace('customers', path='/api/v1/customers', description='Customer operations')
ns_items = Namespace('items', path='/api/v1/items', description='Item operations')
ns_orders = Namespace('orders', path='/api/v1/orders', description='Order operations')
ns_keys = Namespace('keys', path='/api/v1/keys', description="Keys operations")

# add namespaces
api.add_namespace(ns_customers)
api.add_namespace(ns_items)
api.add_namespace(ns_orders)
api.add_namespace(ns_keys)

# Model definitions
get_order_model = api.model('Get Order', {
    'order_id': fields.String(description='The order unique identifier', readonly=True),
    'customer_id': fields.String(description='Customer identifier'),
    'items': fields.List(fields.Nested(api.model('Item', {
        'item_id': fields.String(required=True, description='Item identifier'),
        'name': fields.String(required=True, description='Item name'),
        'quantity': fields.Integer(required=True, description='Quantity of the item'),
        'price': fields.Float(required=True, description='Price of the item')
    })), required=True, description='List of items'),
    'total': fields.Float(required=True, description='Total price of the order'),
    'date': fields.String(required=True, description='Date of the order'),
    'status': fields.String(required=True, description='Status of the order')
})

post_order_model = api.model('Post Order', {
    'customer_id': fields.String(required=True, description='Customer identifier'),
    'items': fields.List(fields.Nested(api.model('Item', {
        'item_id': fields.String(required=True, description='Item identifier'),
        'name': fields.String(required=True, description='Item name'),
        'quantity': fields.Integer(required=True, description='Quantity of the item'),
        'price': fields.Float(required=True, description='Price of the item')
    })), required=True, description='List of items'),
    'total': fields.Float(required=True, description='Total price of the order'),
    'date': fields.String(required=True, description='Date of the order'),
    'status': fields.String(required=True, description='Status of the order')
})

post_customer_model = api.model('Post Customer', {
    'name': fields.String(required=True, description='Full name of the customer'),
    'email': fields.String(required=True, description='Email address of the customer'),
    'password': fields.String(required=True, description='Password for the customer account'),
    'address': fields.String(required=True, description='Physical address of the customer')
})

get_customer_model = api.model('Get Customer', {
    'customer_id': fields.String(required=True, description='The unique identifier for the customer'),
    'name': fields.String(required=True, description='Full name of the customer'),
    'email': fields.String(required=True, description='Email address of the customer'),
    'address': fields.String(required=True, description='Physical address of the customer')
})

get_item_model = api.model('Get Item', {
    'item_id': fields.String(required=True, description='The unique identifier for the item'),
    'name': fields.String(required=True, description='Item name'),
    'price': fields.Float(required=True, description='Item price'),
    'stock': fields.Integer(required=True, description='Item stock count')
})

post_item_model = api.model('Post Item', {
    'name': fields.String(required=True, description='Item name'),
    'price': fields.Float(required=True, description='Item price'),
    'stock': fields.Integer(required=True, description='Item stock count')
})

get_key_model = api.model('Create API Key', {
    'active': fields.Boolean(required=True, description='active key?'),
    'key_id': fields.String(required=True, description='Key id'),
    'key': fields.String(required=True, description='API Key')
})

# Helper function to convert MongoDB documents to JSON-serializable format
def convert_to_json(data):
    if isinstance(data, list):
        return [convert_to_json(item) for item in data]
    if isinstance(data, dict):
        return {k: convert_to_json(v) for k, v in data.items()}
    if isinstance(data, ObjectId):
        return str(data)
    return data

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if not api_key:
            return jsonify({'error': 'API key is missing'}), 401
        
        key_data = mongo.db.api_keys.find_one({'key': api_key, 'active': True})
        if not key_data:
            return jsonify({'error': 'Invalid or inactive API key'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

@ns_orders.route('/')
@ns_orders.route('')
class OrderList(Resource):
    @cross_origin(headers=['Content-Type'])
    def options(self):
        return jsonify(success=True)

    @api.doc('list_orders')
    @api.marshal_list_with(get_order_model)
    # @require_api_key
    def get(self):
        '''List all orders'''
        orders = mongo.db.orders.find()
        return list(orders)

    @api.doc('create_order')
    @cross_origin(headers=['Content-Type'])
    @api.expect(post_order_model)
    @ns_orders.marshal_with(get_order_model, code=201)  # Ensure this uses a model that includes the order_id
    def post(self):
        '''Create a new order'''
        data = request.json
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

        # Ensure ObjectId fields are converted to strings
        return convert_to_json(new_order), 201


@ns_orders.route('/<string:order_id>')
class Order(Resource):
    @api.doc('get_order')
    @api.marshal_with(get_order_model)
    def get(self, order_id):
        '''Get details of a specific order'''
        order = mongo.db.orders.find_one({'order_id': order_id})
        if not order:
            return {'message': 'Order not found'}, 404
        return order

    @api.doc('update_order')
    @api.expect(post_order_model)
    @api.marshal_with(get_order_model)
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


@ns_orders.route('/<string:order_id>/status')
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


@ns_customers.route('/')
@ns_customers.route('')
class CustomerList(Resource):
    @api.doc('list_customers')
    @api.marshal_list_with(get_customer_model)
    def get(self):
        '''List all customers'''
        customers = mongo.db.customers.find({}, {'password': 0})  # Exclude passwords from the query result
        return list(customers)

    @api.doc('register_customer')
    @api.expect(post_customer_model)
    @api.marshal_with(get_customer_model, code=201)
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


@ns_customers.route('/<string:customer_id>')
class Customer(Resource):
    @api.doc('get_customer')
    @api.marshal_with(get_customer_model)
    def get(self, customer_id):
        '''Retrieve a specific customer by their customer ID'''
        customer = mongo.db.customers.find_one({'customer_id': customer_id }, {'password': 0})
        if not customer:
            return {'message': 'Customer not found'}, 404
        return customer
    
    @api.doc('update_customer')
    @api.marshal_with(get_customer_model)
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
    
@ns_items.route('/')
@ns_items.route('')
class itemsList(Resource):
    @api.doc('get_items')
    @api.marshal_list_with(get_item_model)
    def get(self):
        '''Retrieve all items'''
        items = mongo.db.items.find()
        return list(items), 200
    
    @api.doc('add_item')
    @api.expect(post_item_model)
    @api.marshal_with(get_item_model, code=201)
    def post(self):
        '''Add a new item'''
        item = api.payload
        item['item_id'] = str(uuid.uuid4())  # Generate a new UUID for the item
        mongo.db.items.insert_one(item)  # Insert the new item into the database
        return item, 201
    
@ns_items.route('/<string:item_id>')
class Item(Resource):
    @api.doc('get_item')
    @api.marshal_with(get_item_model)
    def get(self, item_id):
        '''Retrieve a specific item by its item ID'''
        item = mongo.db.items.find_one({'item_id': item_id})
        if item:
            return item, 200
        else:
            return {'message': 'Item not found'}, 404
        
    @api.doc('update_item')
    @api.expect(post_item_model)
    @api.marshal_with(get_item_model)
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

@ns_keys.route('/generate')
class Key(Resource):
    @api.marshal_with(get_key_model)
    def post(self):
        new_key = {
            'key_id': str(uuid.uuid4()),
            'customer_id': '502',
            'active': True
        }
        mongo.db.api_keys.insert_one(new_key)
        return {'message': 'API key generated', 'key': new_key['key']}

@app.after_request
def enforce_https_in_redirects(response):
    # Check if the response is a redirect and the scheme is HTTP
    if response.status_code in (301, 302, 303, 307, 308) and request.url.startswith('http://'):
        if not request.url.startswith('http://localhost'):
            # Replace 'http://' with 'https://' in the Location header
            response.headers['Location'] = response.headers['Location'].replace('http://', 'https://', 1)
    return response

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

@app.after_request
def add_security_headers(response):
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response



if __name__ == '__main__':
    app.run(debug=False, port=5000)
