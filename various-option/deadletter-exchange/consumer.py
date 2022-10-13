import pika
import os

from pika.exchange_type import ExchangeType


def dlx_queue_callback(ch, method, properties, body):
    print('Alt: receive new message ' + str(body))


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()  # start a channel

channel.exchange_declare('main-exchange', exchange_type=ExchangeType.direct)
channel.exchange_declare('dlx', exchange_type=ExchangeType.fanout)


channel.queue_declare(queue='main-exchange-queue', arguments={
                      'x-dead-letter-exchange': 'dlx', 'x-message-ttl': 1000})

channel.queue_bind('main-exchange-queue', 'main-exchange', 'test')
channel.queue_declare(queue='dlx-queue')  # declare queue
channel.queue_bind('dlx-queue', 'dlx')

channel.basic_consume(
    'dlx-queue',
    dlx_queue_callback,
    auto_ack=True)

print('Waiting for messages:')
channel.start_consuming()
