# OrdaSys

## Introduction
OrdaSys is an Order Management System designed to streamline and optimize the management of orders for restaurants and food service providers. It provides a comprehensive suite of tools for managing orders, inventory, and customer data, all accessible via a user-friendly web interface.

## Features
- **Order Tracking:** Track orders from placement through fulfillment.
- **Inventory Management:** Keep tabs on stock levels, manage reorders, and update product details.
- **Customer Management:** Maintain detailed customer profiles, order history, and preferences.
- **Reporting:** Generate detailed reports on sales, customer orders, and inventory status.
- **Multi-user Support:** Different access levels for staff, managers, and administrators.

## Technologies
OrdaSys is built using the following technologies:
- **Frontend:** Vue.js
- **Backend:** Python Flask
- **Database:** MongoDB
- **Containerization:** Podman
- **API Documentation:** Swagger (OpenAPI)

## Prerequisites
Before you can run OrdaSys, make sure you have the following installed:
- Podman (or Docker)
- Python 3.8+
- Node.js 14.x+
- MongoDB

## Run
$ `python3 -m venv venv` \
$ `source venv/bin/activate` \
$ `podman-compose build` \
$ `podman-compose up`

when done do the following after `ctrl` + `c`: \
$ `podman-compose down`
