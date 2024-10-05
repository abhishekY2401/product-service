# Product Microservice

This microservice handles product management, including adding, updating, and retrieving product information. It communicates with the Order microservices through event-driven architecture using RabbitMQ.

## 💡 Features

- Product Management: Create, read, update, and delete product information.
- Event-Driven Architecture: Emits events to RabbitMQ to synchronize product inventory with the Order microservice.
- GraphQL API: Provides a flexible API for product-related queries and mutations.

## ⚙️ Setup Instructions

### 1. Clone the Repository
    
    git clone https://github.com/yourusername/product-service.git
    cd product-service
    

### 2. Install Dependencies
Create a virtual environment and install the required Python dependencies:

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

### 3. Database Setup
Ensure PostgreSQL is running, and configure the config.py with your database connection details:

    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/products_db'

Run database migrations:

    flask db upgrade

### 4. RabbitMQ Setup
Ensure RabbitMQ is running, and update config.py if necessary:

    RABBITMQ_URL = 'amqp://guest:guest@localhost:5672/'

### 5. Environment Variables
Create a .env file to store your environment variables:

    JWT_SECRET_KEY=your_jwt_secret_key
    POSTGRES_USER=your_postgres_user
    POSTGRES_PASSWORD=your_postgres_password
    POSTGRES_DB=user_db
    RABBITMQ_URL=your_rabbitmq_url

### 6. Running the Microservice
To start the service locally:

    flask run --host='0.0.0.0' --port='7000'

### 7. GraphQL Playground
Once the service is running, access the GraphQL playground at 
    
    http://localhost:7000/graphql

## 🔍 GraphQL API

Mutations:

- Add Product: Create a new product.
```
  mutation {
  addProduct(name: "Sample Product", price: 29.99, stock: 100) {
    success
    message
    product {
      id
      name
      price
      stock
    }
  }
}
```

- Update Product: Update product information.
```
  mutation {
    updateProduct(id: 1, name: "Updated Product", price: 19.99, stock: 50) {
      success
      message
    }
  }

```

Queries

- Get Products: Retrieve a list of products.
```
  query {
    getProducts {
      id
      name
      price
      stock
    }
  }

```

- Get Product by ID: Retrieve product details by ID.
```
  query {
    getProduct(id: 1) {
      id
      name
      price
      stock
    }
  }
```

- 

🔐 JWT Protection
All protected queries and mutations require a valid JWT token. Pass it as a Bearer token in the headers:
```
  Authorization: Bearer <your_jwt_token>
```


## 📡 Event-Driven Architecture

1. ```product.added```: Emitted when a new product is added. This event is consumed by the Order microservice to update the product inventory.

2. ```inventory.updated```: Emitted when a product is updated. This event is also consumed by the Order microservice to synchronize product data.

To test this event driven architecture, you can follow the same steps for other microservices and run the following command in Order microservice:
```
python consumer.py
```

## 🐇 RabbitMQ Configuration

- Go to [RabbitMQ](https://www.cloudamqp.com/) site and sign up with google.
- Create a new instance and start the instance server.
- Once this is done, you will be directed to dashboard from there copy the URL from AQMP Details Section.
- Ensure RabbitMQ is properly configured with an exchange and queue for event communication.

## 🛠️ Troubleshooting

- PostgreSQL or RabbitMQ not running: Ensure that PostgreSQL and RabbitMQ services are running before starting the microservice.
- Environment Variables: Double-check the .env file for any misconfigurations.
