import pika
import os
import uuid


def on_request_message_received(ch, method, properties, body):
    print(f'request message: {properties.correlation_id}')
    ch.basic_publish('', routing_key=properties.reply_to,
                     body=f'Hey its your reply to {properties.correlation_id}')


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)

connection = pika.BlockingConnection(connection_params)

channel = connection.channel()  # start a channel

reply_queue = channel.queue_declare(queue='request-queue')

channel.basic_consume(queue='request-queue',
                      auto_ack=True, on_message_callback=on_request_message_received)

print('Starting server')

channel.start_consuming()
