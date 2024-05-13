#!/usr/bin/python3
"""Module that defines all the models"""

from flask import Flask
from flask_restx import Api, fields

app = Flask(__name__)
api = Api(app)

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
