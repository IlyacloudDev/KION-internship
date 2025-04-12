import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


from pika import BlockingConnection, ConnectionParameters, PlainCredentials
import json
from .services.deduplicate_service import is_duplicate_event
from .services.product_event_service import _create_product_event


def process_product_event(channel, method, properties, body):
    """
    Handles incoming product events data from RabbitMQ queue.
    """
    product_event = json.loads(body)
    if not is_duplicate_event(product_event):
        _create_product_event(product_event_data=product_event)
    channel.basic_ack(delivery_tag=method.delivery_tag)



def product_event_consumer():
    """
    RabbitMQ consumer process product events and sends the product event to the deduplication engine.
     """
    connection_params = ConnectionParameters(
        host=os.environ.get('RABBITMQ_HOST'),
        port=int(os.environ.get('RABBITMQ_PORT')),
        credentials=PlainCredentials(os.environ.get('RABBITMQ_DEFAULT_USER'), os.environ.get('RABBITMQ_DEFAULT_PASS'))
    )
    with BlockingConnection(connection_params) as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue='product_events', durable=True)

            channel.basic_consume(
                queue='product_events',
                on_message_callback=process_product_event,
            )
            channel.start_consuming()


if __name__ == '__main__':
    product_event_consumer()
