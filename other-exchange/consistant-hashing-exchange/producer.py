import pika
import os
from pika.exchange_type import ExchangeType


url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()  # start a channel


channel.exchange_declare('simple-hashing', 'x-consistent-hash')

# create binding between queue and exchange
routing_key = "1221H3423fsd ds2  assd13124sdh me!"

message = 'this is the core message'

# publish message
channel.basic_publish(
    exchange='simple-hashing',
    routing_key=routing_key,
    body=message)

print('Message sent.')

channel.close()
connection.close()
