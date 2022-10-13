import pika
import os
import uuid


def callback(ch, method, properties, body):
    print('Received ' + str(body))


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
    'CLOUDAMQP_URL', 'amqps://epxjsryr:d51jZ0NquNgSlDCMxW04vIeOkiOXYSMl@mini-grey-macaw.rmq3.cloudamqp.com/epxjsryr')
connection_params = pika.URLParameters(url)

connection = pika.BlockingConnection(connection_params)

channel = connection.channel()  # start a channel

reply_queue = channel.queue_declare(queue='', exclusive=True)

channel.basic_consume(queue=reply_queue.method.queue,
                      auto_ack=True, on_message_callback=callback)

channel.queue_declare(queue='request-queue')
message = 'Can I request a reply?'

cor_id = str(uuid.uuid4())

print(f'Sending Request: {cor_id}')

channel.basic_publish(exchange='', routing_key='request-queue', body=message,
                      properties=pika.BasicProperties(reply_to=reply_queue.method.queue, correlation_id=cor_id))

print('Waiting for messages:')

channel.start_consuming()
