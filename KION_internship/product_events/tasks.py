import os
from celery import shared_task
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
import json


@shared_task
def send_to_rabbitmq(product_event_data):
    """
    Celery task to send a validated product event to RabbitMQ.
    """
    connection = BlockingConnection(
        ConnectionParameters(
            host=os.environ.get('RABBITMQ_HOST'),
            port=os.environ.get('RABBITMQ_PORT'),
            credentials=PlainCredentials(os.environ.get('RABBITMQ_DEFAULT_USER'), os.environ.get('RABBITMQ_DEFAULT_PASS'))
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='product_events')

    channel.basic_publish(
        exchange='',
        routing_key='product_events',
        body=json.dumps(product_event_data)
    )
    connection.close()

