from app.models import Product, db
from app.rabbitmq import consume_events, publish_event
from main import app
from config import Config
import json
import logging


def update_inventory_on_order_placed(order_data):
    try:
        with app.app_context():
            products = order_data['items']
            event_data = []

            for item in products:
                product_id = item['product_id']
                quantity_ordered = item['quantity']

                product = Product.query.filter_by(id=product_id).first()

                if product:
                    product.stock -= quantity_ordered
                    db.session.commit()

                    logging.info(
                        f"Updated inventory for product_id {product_id}. New quantity: {product.stock}")

                    event_data.append({
                        "product_id": product.id,
                        "quantity": product.stock
                    })

                else:
                    logging.warning(
                        f"Product not found for product_id {product_id}")

            publish_event(exchange_name="event_exchange",
                          routing_key=Config.INVENTORY_UPDATED_QUEUE, message=json.dumps(event_data))
            logging.info(
                f"Emit event data to update inventory in orders: {event_data}")

    except Exception as error:
        logging.error(f"Error while updating inventory: {error}")


def on_message_received(ch, method, properties, body):
    logging.info(f"Received event: {body}")

    event_data = json.loads(body)
    event_type = method.routing_key

    if event_type == 'order.placed':
        update_inventory_on_order_placed(event_data)
    else:
        logging.warning(f"Unhandled event type: {event_type}")


if __name__ == '__main__':
    consume_events(on_message_received)
