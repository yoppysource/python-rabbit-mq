from json import JSONDecoder, JSONEncoder
import pika
import os
from pika.exchange_type import ExchangeType

url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()  # start a channel

# channel.exchange_declare(exchange='mytopicexchange',
#                          exchange_type=ExchangeType.topic)

user_payments_message = {"message": "hello"}
jsonfile = JSONEncoder().encode(user_payments_message)
# publish message
channel.basic_publish(
    body=jsonfile,
    exchange='amq.topic',
    routing_key='iot.planters.23fdsjfdf.snapshot'
)
print('Message sent.')

channel.close()
connection.close()
