# Project Name
OrdaSys

## Introduction
OrdaSys is an Order Management System designed to streamline and optimize the management of orders for restaurants and food service providers. It provides a comprehensive suite of tools for managing orders, items, and customer data, all accessible via a user-friendly web interface.
[Link to Deployed Site](https://orda-v1-0-frontend.onrender.com)
[Final Project Blog Article](https://medium.com/@cxnpyrvrd/building-ordasys-a-journey-through-developing-an-order-management-system-5fbfcd72e9ad)
[Author(s) Linkedin](https://www.linkedin.com/in/phiwokuhleshongwe) | [Linkedin](https://www.linkedin.com/in/hassan-muhammad-5804baa3)

## Installation
To get started with  OrdaSys, make sure you have the following installed:

- Podman (or Docker)
- Python 3.8+
- Node.js 14.x+ (Bun)
- MongoDB
- Clone the repository to your local machine.

## MongoDB setup locally and anywhere else

You need to set the following in your ~/.zshrc or ~/.bashrc file

```
export MONGO_USER='yourMongoUsername'
export MONGO_PASSWORD='yourMongoPassword'
export MONGO_HOST='yourMongoHost'
export MONGO_DBNAME='yourMongoDbName'
```

Once set then run:

$ `source ~/.zshrc`

OR

$ `source ~/.bashrc`

depending on the shell you're using.

## Run
$ `python3 -m venv venv` \
$ `source venv/bin/activate` \
$ `podman-compose build` \
$ `podman-compose up`

When done do the following `ctrl` + `c` then do: \
$ `podman-compose down`

## Usage
OrdaSys offers a range of features designed to meet the needs of business owners:

- **Order Tracking:** Track orders from placement through fulfillment.
- **items Management:** Keep tabs on stock levels, manage reorders, and update product details.
- **Customer Management:** Maintain detailed customer profiles, order history, and preferences.
- **Reporting:** Generate detailed reports on sales, customer orders, and items status.
- **Multi-user Support:** Different access levels for staff, managers, and administrators.

## Contributing
Contributions to OrdaSys are welcome, Please feel free to submit pull requests or report issues on the repository.

## Related Projects
[OMSMiniProject](https://github.com/rsrahul1000/OMSMiniProject)

## Licensing
OrdaSys is licensed under the MIT License. See the LICENSE file for details.
