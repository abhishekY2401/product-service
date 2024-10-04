import json
import logging
from datetime import datetime, timezone
from ariadne import QueryType, MutationType
from app.middleware import jwt_required
from app.models import Product
from config import Config
from app.extensions import db, bcrypt
from app.rabbitmq import publish_event

query = QueryType()
mutation = MutationType()


@query.field("products")
@jwt_required
def fetch_products(*_):
    try:
        products = Product.query.all()
        return products
    except Exception as e:
        logging.error(f"Error fetching products: {e}")
        return []

# fetch a product by its id


@query.field("product")
@jwt_required
def fetch_product(_, info, id):
    try:
        # product_id = info.context.get("product_id")
        product = Product.query.get(id)
        if not product:
            raise Exception(f"Product with id {id} not found")
        return product
    except Exception as e:
        logging.error(f"Error fetching product: {e}")
        return None


@query.field("productByIds")
@jwt_required
def resolve_product_by_ids(_, info, ids):
    # fetch all the product prices based on the product ids
    products = Product.query.filter(Product.id.in_(ids)).all()

    return [product.to_dict() for product in products]

# handle creation of product


@mutation.field("createProduct")
@jwt_required
def handle_create_product(_, info, input):
    name = input.get('name'),
    description = input.get('description'),
    price = input.get('price'),
    stock = input.get('stock'),
    sku = input.get('sku')
    category = input.get('category')

    if not name or not description or not price or not stock or not sku or not category:
        raise Exception("Please enter all the product data")

    try:
        if Product.query.filter_by(sku=sku).first():
            raise Exception('Product with this sku number already exists!')

        new_product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            sku=sku,
            category=category,
        )

        db.session.add(new_product)
        db.session.commit()
        logging.info(f"new product stored in database")

        event_data = json.dumps({
            "id": new_product.id,
            "name": new_product.name,
            "price": new_product.price,
            "quantity": new_product.stock,
        })
        publish_event(exchange_name="event_exchange",
                      routing_key=Config.PRODUCT_CREATED_QUEUE, message=event_data)

        return new_product

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while creating product: {e}")
        raise Exception("Failed to create a product.")


@mutation.field("updateProductInventory")
@jwt_required
def update_product_inventory(_, info, product_id, stock_change):
    try:
        logging.info(f"Attempting to find product with id: {product_id}")
        product = Product.query.get(product_id)

        if not product:
            logging.error(f"Product with id {product_id} not found")
            raise Exception("Product not found")

        logging.info(f"Found product: {product}")

        # Check stock to avoid negative values (if applicable to your business logic)
        if product.stock + stock_change < 0:
            logging.error(
                f"Insufficient stock for product {product_id}. Current stock: {product.stock}, attempted change: {stock_change}")
            raise Exception("Insufficient stock to complete the operation")

        # Update the stock
        product.stock += stock_change
        logging.info(
            f"Updated stock for product {product_id}. New stock: {product.stock}")

        # Emit the "Inventory Updated" event
        event_data = json.dumps({
            'product_id': product.id,
            'new_stock': product.stock
        })

        # Try publishing the event before committing the transaction
        try:
            publish_event(Config.INVENTORY_UPDATED_QUEUE, event_data)
            logging.info(
                f"Published event for product {product_id} to queue {Config.INVENTORY_UPDATED_QUEUE}")
        except Exception as event_error:
            logging.error(
                f"Failed to publish event for product {product_id}: {event_error}")
            raise Exception("Failed to publish inventory update event")

        # Commit the transaction only if the event was successfully published
        db.session.commit()
        logging.info(
            f"Transaction committed successfully for product {product_id}")

        payload = {
            "success": True,
            "product": product.to_dict()
        }

    except Exception as error:
        logging.error(
            f"Error updating product inventory for product {product_id}: {error}")
        db.session.rollback()  # Rollback to previous state in case of any exception
        return {
            "success": False,
            "errors": str(error),
        }

    return payload
