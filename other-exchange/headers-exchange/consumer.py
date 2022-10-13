import pika
import os
from pika.exchange_type import ExchangeType


def callback(ch, method, properties, body):
    print('Received ' + str(body))


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()  # start a channel

channel.exchange_declare(exchange='header-exchange',
                         exchange_type=ExchangeType.headers)

channel.queue_declare(queue='letterbox')

bind_args = {
    'x-match': 'all',  # any면 두개중 하나만 맞아도 된다
    'name': 'brian',
    'age': '53', }

channel.queue_bind('letterbox', 'header-exchange', arguments=bind_args)

channel.basic_consume(
    queue='letterbox',
    on_message_callback=callback,
    auto_ack=True)

print('Waiting for messages:')
channel.start_consuming()
