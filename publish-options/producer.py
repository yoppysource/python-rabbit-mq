import pika
import os
from pika.exchange_type import ExchangeType

url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()  # start a channel

channel.confirm_delivery()  # Enables Pulish Confirms

channel.tx_select()  # Enables Transcations

# define name and type for exchange
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

# Creates a durable queue that survives restarts
channel.queue_declare("text", durable=True)

message = "Hello I want to broadcast this message"

# publish message
channel.basic_publish(
    body=message,
    exchange='pubsub',
    properties=pika.BasicProperties(
        headers={'name': 'brian'},
        delivery_mode=1,
        expiration=1234123,
        content_type="application/json",
    ),
    routing_key='',
    mandatory=True
)

channel.tx_commit()  # commit a transaction
channel.tx_rollback()  # rollback a transaction

print('Message sent.')

channel.close()
connection.close()
