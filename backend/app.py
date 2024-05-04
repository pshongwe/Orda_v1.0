#!/usr/bin/python3
import os
import uuid
import logging
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_restx import Api, Resource, fields


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
api = Api(app, version='1.0', title='API Documentation', description='A simple API', doc='/swagger/')

# Model definitions
get_model = api.model('Order', {
    'order_id': fields.Integer(description='The order unique identifier', readonly=True),
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


@api.route('/api/orders')
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


@api.route('/api/orders/<string:order_id>')
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


@api.route('/api/orders/<string:order_id>/status')
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


@api.route('/api/customers')
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


@api.route('/api/customers/<string:customer_id>')
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
