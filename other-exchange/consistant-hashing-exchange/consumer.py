import pika
import os
from pika.exchange_type import ExchangeType


def on_message1_received(ch, method, properties, body):
    print('queue 1: ' + str(body))


def on_message2_received(ch, method, properties, body):
    print('queue 2: ' + str(body))


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()  # start a channel

channel.exchange_declare('simple-hashing', 'x-consistent-hash')

channel.queue_declare(queue='letterbox1')
channel.queue_declare(queue='letterbox2')
channel.basic_consume(
    queue='letterbox1',
    on_message_callback=on_message1_received,
    auto_ack=True)

channel.queue_bind('letterbox1', 'simple-hashing', routing_key='1')
channel.queue_bind('letterbox2', 'simple-hashing', routing_key='4')

channel.basic_consume(
    queue='letterbox2',
    on_message_callback=on_message2_received,
    auto_ack=True)


print('Waiting for messages:')
channel.start_consuming()
