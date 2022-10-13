import pika
import os


def callback(ch, method, properties, body):
    print('Received ' + str(body))


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()  # start a channel

channel.queue_declare(queue='letterbox')  # declare queue

channel.basic_consume(
    'letterbox',
    callback,
    auto_ack=True)

print('Waiting for messages:')
channel.start_consuming()
connection.close()
