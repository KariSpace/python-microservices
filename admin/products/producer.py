import pika

params = pika.URLParameters('amqps://wqcqaqin:GL8aGVdApoUXWnl7NrCqojT-4rUauyQZ@jackal.rmq.cloudamqp.com/wqcqaqin')

connection = pika.BlockingCommection(params)

channel = connection.channel()

def publish():
    channel.basic_publish(exchange='', routing_key='main', body='hello')