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

channel.exchange_declare(exchange='second-exchange',
                         exchange_type=ExchangeType.fanout)

channel.queue_declare(queue='letterbox')

channel.queue_bind('letterbox', 'second-exchange')

channel.basic_consume(
    'letterbox',
    callback,
    auto_ack=True)

print('Waiting for messages:')
channel.start_consuming()
connection.close()
