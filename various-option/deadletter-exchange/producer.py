import pika
import os
from pika.exchange_type import ExchangeType

# Producer에서 보낸 메세지가 메인 exchange에서 어떤 큐에도 올라가지 않는다면 alter exchange로 이동한당

url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()  # start a channel

channel.exchange_declare('main-exchange', exchange_type=ExchangeType.direct)

message = "This message will expire..."

# publish message
channel.basic_publish(
    body=message,
    exchange='main-exchange',
    routing_key='test'
)
print('Message sent.')

channel.close()
connection.close()
