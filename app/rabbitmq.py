import pika
import logging
from config import Config


def setup_rabbitmq_connection():
    try:
        connection = pika.BlockingConnection(
            pika.URLParameters(Config.RABBITMQ_URL))
        return connection
    except Exception as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")
        return None

# publish an event to queue


def publish_event(queue_name, message):
    connection = setup_rabbitmq_connection()

    if not connection:
        return None

    try:
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        logging.info(f"Published message to {queue_name}: {message}")

    finally:
        connection.close()


# listen to events sent from different microservice
def listen_events(queue_name, callback):
    connection = setup_rabbitmq_connection()

    if not connection:
        return None

    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    def on_message(channel, method, properties, body):
        logging.info(f"Received message from {queue_name}: {body}")
        callback(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=on_message)
    logging.info(f"Listening for messages on {queue_name}...")
    channel.start_consuming()
