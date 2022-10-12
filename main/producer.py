from crypt import methods
import json
import pika

params = pika.URLParameters('amqps://wqcqaqin:GL8aGVdApoUXWnl7NrCqojT-4rUauyQZ@jackal.rmq.cloudamqp.com/wqcqaqin')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)

    return(' [x] Sent ')

    # connection.close()