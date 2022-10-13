import pika
import os
from pika.exchange_type import ExchangeType


url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()  # start a channel

channel.exchange_declare(exchange='header-exchange',
                         exchange_type=ExchangeType.headers)
# create binding between queue and exchange
message = "Hello this is message sent with headers"

# publish message
channel.basic_publish(
    exchange='header-exchange',
    routing_key='',
    body=message,
    properties=pika.BasicProperties(headers={'name': 'brian'}))

print('Message sent.')

channel.close()
connection.close()
