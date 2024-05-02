import os
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

# Model definition
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
