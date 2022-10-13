import pika
import os
from pika.exchange_type import ExchangeType


url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()  # start a channel

channel.exchange_declare(exchange='first-exchange',
                         exchange_type=ExchangeType.direct)

channel.exchange_declare(exchange='second-exchange',
                         exchange_type=ExchangeType.fanout)

channel.exchange_bind('second-exchange', 'first-exchange')
# create binding between queue and exchange
message = "This message has gone through multiple exchanges"

channel.basic_publish(exchange='first-exchange', routing_key='', body=message)

print(f'sent message {message}')

connection.close()
