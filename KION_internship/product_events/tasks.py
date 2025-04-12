import os
from celery import shared_task
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
import json


@shared_task
def send_product_event_to_rabbitmq(product_event_data):
    """
    Celery task to send a validated product event to RabbitMQ.
    """
    connection_params = ConnectionParameters(
        host=os.environ.get('RABBITMQ_HOST'),
        port=int(os.environ.get('RABBITMQ_PORT')),
        credentials=PlainCredentials(os.environ.get('RABBITMQ_DEFAULT_USER'), os.environ.get('RABBITMQ_DEFAULT_PASS'))
    )
    with BlockingConnection(connection_params) as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue='product_events', durable=True)

            channel.basic_publish(
                exchange='',
                routing_key='product_events',
                body=json.dumps(product_event_data)
            )
