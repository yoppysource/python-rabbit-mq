from urllib import request
import pika
import os

from pika.exchange_type import ExchangeType


def on_message_callback(ch, method, properties, body):
    if(method.delivery_tag % 5 == 0):
        ch.basic_nack(delivery_tag=method.delivery_tag,
                      requeue=False, multiple=True)
    print('receive new message ' + str(body))


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()  # start a channel

channel.exchange_declare('accept-reject-exchange',
                         exchange_type=ExchangeType.fanout)
channel.queue_declare(queue='letterbox')

channel.queue_bind('letterbox', 'accept-reject-exchange')

channel.basic_consume(
    queue='letterbox',
    on_message_callback=on_message_callback, auto_ack=False)

print('Waiting for messages:')
channel.start_consuming()
