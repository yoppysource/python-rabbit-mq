import pika
import os
import time
import random


def callback(ch, method, properties, body):
    processing_time = random.randint(1, 6)
    print(f'received: {body}, will take {processing_time} to process')
    time.sleep(processing_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # which message want to ack
    print("Finished processing the message")


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()  # start a channel

channel.queue_declare(queue='letterbox')  # declare queue

# limit consumer to prefetch only 1 message
#! this logic is crucial. It allow to broker to wait deliver message to acked consumer
#! If not, it when just deliver one by one. i.e. (1,3,5,7...) (2,4,6,8 ...)
channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    'letterbox',
    callback,
    auto_ack=False)

print('Waiting for messages:')
channel.start_consuming()
connection.close()
