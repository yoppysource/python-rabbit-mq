import pika
import os
import time
import random

url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()  # start a channel

channel.queue_declare(queue='letterbox')  # declare queue
# create binding between queue and exchange

messageId = 1

while(True):
    message = f"Sending messageId: {messageId}"
    channel.basic_publish(
        body=message,
        exchange='',
        routing_key='letterbox')

    print(f'Message sent.{message}')

    time.sleep(random.randint(1, 3))

    messageId += 1
