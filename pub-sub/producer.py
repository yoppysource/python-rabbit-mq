import pika
import os
from pika.exchange_type import ExchangeType

url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()  # start a channel

# define name and type for exchange
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

message = "Hello I want to broadcast this message"

# publish message
channel.basic_publish(
    body=message,
    exchange='pubsub',
    routing_key=''
)
print('Message sent.')

channel.close()
connection.close()
