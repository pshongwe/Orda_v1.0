import os
from pymongo import MongoClient

# Connection URI
client = MongoClient(f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}/{os.getenv('MONGO_DBNAME')}?retryWrites=true&w=majority")

# Select the database
db = client[f"{os.getenv('MONGO_DBNAME')}"]

# Data to be inserted
customers = [
    {"customer_id": "501", "name": "John Doe", "email": "john.doe@example.com", "address": "123 Elm St, Somewhere, USA"},
    {"customer_id": "502", "name": "Jane Smith", "email": "jane.smith@example.com", "address": "456 Oak St, Anytown, USA"}
]

orders = [
    {
        "order_id": "1001",
        "customer_id": "501",
        "items": [
            {"item_id": "101", "quantity": 2, "price": 25.50},
            {"item_id": "105", "quantity": 1, "price": 5.75}
        ],
        "total": 56.75,
        "date": "2024-04-15",
        "status": "Shipped"
    },
    {
        "order_id": "1002",
        "customer_id": "502",
        "items": [
            {"item_id": "103", "quantity": 1, "price": 15.00}
        ],
        "total": 15.00,
        "date": "2024-04-16",
        "status": "Pending"
    }
]

items = [
    {"item_id": "101", "name": "Widget A", "price": 25.50, "stock": 50},
    {"item_id": "103", "name": "Widget C", "price": 15.00, "stock": 35},
    {"item_id": "105", "name": "Widget E", "price": 5.75, "stock": 100}
]

# Insert data into collections
db.customers.insert_many(customers)
db.orders.insert_many(orders)
db.items.insert_many(items)

print("Data inserted successfully!")

