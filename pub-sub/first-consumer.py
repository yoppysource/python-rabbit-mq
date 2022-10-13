import pika
import os
from pika.exchange_type import ExchangeType


def callback(ch, method, properties, body):
    print('first consumer received new message:' + str(body))


# url = os.environ.get(
#     'CLOUDAMQP_URL', ' amqps://127.0.0.1:5672')
# connection_params = pika.URLParameters('amqps://127.0.0.1:5672')
connection_params = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_params)

channel = connection.channel()  # start a channel

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
