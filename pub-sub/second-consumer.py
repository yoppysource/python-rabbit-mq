import pika
import os
from pika.exchange_type import ExchangeType


def callback(ch, method, properties, body):
    print('second consumer received new message:' + str(body))


url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()  # start a channel

# Binding 하기 전에 exchange가 먼저 생성되어야 함
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

# ''으로 브로커가 랜덤으로 만들라고 선언, exclusive=True로 close되면 큐 삭제되게 설정
queue = channel.queue_declare(queue='', exclusive=True)

# 큐를 exchange와 바인딩
channel.queue_bind(exchange='pubsub', queue=queue.method.queue)

channel.basic_consume(
    queue=queue.method.queue,
    on_message_callback=callback,
    auto_ack=True)

print('Waiting for messages:')
channel.start_consuming()
