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
model = api.model('Order', {
    'order_id': fields.Integer(description='The order unique identifier', readonly=True)
})

@api.route('/api/orders')
class OrderList(Resource):
    
    @api.doc('list_orders')
    @api.marshal_list_with(model)
    def get(self):
        '''List all orders'''
        orders = mongo.db.orders.find()
        return list(orders)

    @api.doc('create_order')
    @api.expect(model)
    @api.marshal_with(model, code=201)
    def post(self):
        '''Create a new order'''
        data = api.payload
        if not data:
            api.abort(400, "No data provided")
        order = mongo.db.orders.insert_one({
            'name': data['name'],
            'quantity': data['quantity']
        })
        new_order = mongo.db.orders.find_one({'_id': order.inserted_id})
        return new_order, 201

if __name__ == '__main__':
    app.run(debug=True, port=5001)
