import pika
from pika.exchange_type import ExchangeType
import os


def callback(ch, method, properties, body):
    print('analytics service: ' + str(body))


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')

connection_params = pika.URLParameters(url)

connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

channel.exchange_declare(exchange='mytopicexchange',
                         exchange_type=ExchangeType.topic)

queue = channel.queue_declare(queue='', exclusive=True)

channel.queue_bind(exchange='mytopicexchange', queue=queue.method.queue,
                   routing_key='user.#')

channel.basic_consume(
    queue=queue.method.queue,
    on_message_callback=callback,
    auto_ack=True)

print('Waiting for messages:')
channel.start_consuming()
connection.close()
