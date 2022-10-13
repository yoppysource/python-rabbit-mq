import pika
import os


url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()  # start a channel

channel.queue_declare(queue='letterbox')  # declare queue
# create binding between queue and exchange
message = "Hello this is my first message"

# publish message
channel.basic_publish(
    body=message,
    exchange='',
    routing_key='letterbox'
)
print('Message sent.')

channel.close()
connection.close()
