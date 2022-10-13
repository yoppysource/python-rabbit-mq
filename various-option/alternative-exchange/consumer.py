import pika
import os

from pika.exchange_type import ExchangeType


def alt_queue_callback(ch, method, properties, body):
    print('Alt: receive new message ' + str(body))


def main_queue_callback(ch, method, properties, body):
    print('Main: receive new message ' + str(body))


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()  # start a channel

channel.exchange_declare('alter-exchange', exchange_type=ExchangeType.fanout)
channel.exchange_declare('main-exchange', exchange_type=ExchangeType.direct, arguments={
    'alternate-exchange': 'alter-exchange'
})

channel.queue_declare(queue='alter-exchange-queue')  # declare queue
channel.queue_bind('alter-exchange-queue', 'alter-exchange')
channel.basic_consume(
    'alter-exchange-queue',
    alt_queue_callback,
    auto_ack=True)

channel.queue_declare(queue='main-exchange-queue')  # declare queue
channel.queue_bind('main-exchange-queue', 'main-exchange', 'test')
channel.basic_consume(
    'main-exchange-queue',
    main_queue_callback,
    auto_ack=True)

print('Waiting for messages:')
channel.start_consuming()
connection.close()
