#!/usr/bin/python3
import unittest
from app import app, api
from pymongo import MongoClient
import mongomock
import json


class BasicTests(unittest.TestCase):

    def setUp(self):
        # Create a Flask test client
        self.app = app.test_client()

        # Propagate the exceptions to the test client
        self.app.testing = True

        # Use mongomock to mock the MongoDB connection
        with mongomock.patch(servers=(('server.example.com', 27017),)):
            self.mock_client = MongoClient('server.example.com')
            self.mock_db = self.mock_client['test_db']
            app.config['MONGO_URI'] = 'mongodb://server.example.com:27017/test_db'
            self.db = MongoClient(app.config["MONGO_URI"]).db

    def test_get_orders(self):
        """Test the /api/orders GET endpoint"""
        # Assuming you have a function to insert data for testing
        self.db.orders.insert_one({'order_id': '1', 'customer_id': 'c1', 'items': [], 'total': 0, 'date': '2024-04-15', 'status': 'Collected'})
        
        response = self.app.get('/api/orders')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Collected', str(response.data))

    def test_post_order(self):
        """Test the /api/orders POST endpoint"""
        order_data = {
            'customer_id': 'c1',
            'items': [{'item_id': 'i1', 'quantity': 1, 'price': 10.0}],
            'total': 10.0,
            'date': '2024-04-15',
            'status': 'Pending'
        }
        response = self.app.post('/api/orders', json=order_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Pending', str(response.data))

    def test_get_customer(self):
        """Test the /api/customers/<customer_id> GET endpoint"""
        self.db.customers.insert_one({'customer_id': 'c1', 'name': 'John Doe', 'email': 'john@example.com', 'password': 'hashedpass', 'address': '123 Elm St'})
        
        response = self.app.get('/api/customers/c1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('John Doe', str(response.data))

    def test_register_customer(self):
        """Test the /api/customers POST endpoint for registering a new customer"""
        new_customer = {
            'name': 'Alice Smith',
            'email': 'alice@example.com',
            'password': 'securePassword123',
            'address': '456 Tree St'
        }
        response = self.app.post('/api/customers', json=new_customer)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Alice Smith', str(response.data))

    def test_update_order(self):
        """Test the /api/orders/<order_id> PUT endpoint for updating an existing order"""
        # Assuming order_id '1' exists from test setup or previous test
        update_data = {
            'status': 'Shipped'
        }
        response = self.app.put('/api/orders/1', json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Shipped', str(response.data))

    def test_delete_order(self):
        """Test the /api/orders/<order_id> DELETE endpoint for deleting an order"""
        # Ensure an order exists to delete
        response = self.app.delete('/api/orders/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Order deleted successfully', str(response.data))

    def test_get_order_status(self):
        """Test the /api/orders/<order_id>/status GET endpoint"""
        # Ensure the order with specific status exists
        response = self.app.get('/api/orders/1/status')
        self.assertEqual(response.status_code, 200)
        # Check for specific status in the response
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_data['status'], 'Collected')

    def test_update_order_status(self):
        """Test the /api/orders/<order_id>/status PUT endpoint"""
        status_update = {'status': 'Delivered'}
        response = self.app.put('/api/orders/1/status', json=status_update)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_data['status'], 'Delivered')


if __name__ == '__main__':
    unittest.main()
