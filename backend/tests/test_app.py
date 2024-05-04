#!/usr/bin/python3
import unittest
from app import app, api
from pymongo import MongoClient
import mongomock
import json


class OrdaSysTests(unittest.TestCase):
    def setUp(self):
        # Patch the PyMongo client used in your application
        self.patcher = mongomock.patch(servers=(('fake_server.example.com', 27017),))
        self.patcher.start()
        
        # Setup your Flask test client
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        # Use mongomock to create a fake database
        self.mongo_client = mongomock.MongoClient('mongodb://fake_server.example.com:27017')
        self.db = self.mongo_client.db  # Adjust 'db' based on how it's called in your app

    def tearDown(self):
        self.patcher.stop()

    def test_delete_order(self):
        # Pre-populate mock data
        self.db.orders.insert_one({'order_id': '1', 'details': 'Some details'})
        
        # Perform the test
        response = self.app.delete('/api/orders/1')
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        result = self.db.orders.find_one({'order_id': '1'})
        self.assertIsNone(result)

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
