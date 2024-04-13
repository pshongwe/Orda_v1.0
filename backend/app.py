import logging
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_restx import Api, Resource, fields


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/order_management"
mongo = PyMongo(app)
CORS(app)
# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
api = Api(app)

# Model definition
model = api.model('Order', {
    'id': fields.Integer(description='The order unique identifier', readonly=True),
    'name': fields.String(required=True, description='Name of the order'),
    'quantity': fields.Integer(required=True, description='Quantity of the order')
})

@api.route('/api/data')
class OrderList(Resource):
    @api.doc('list_orders')
    @api.marshal_list_with(model)
    def get(self):
        '''List all orders'''
        return [{'id': 1, 'name': 'Sample Order', 'quantity': 10}]


if __name__ == '__main__':
    app.run(debug=True, port=5001)
