import queue
import pika

params = pika.URLParameters('amqps://yjhqxoyp:VZ8jfFcGrtSlMH1McSOqJQgMDS0zhl05@shrimp.rmq.cloudamqp.com/yjhqxoyp')

connection = pika.BlockingCommection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('reseived admin')
    print(body)

channel.basic_consume(queue = 'admin', on_message_callback=callback)
print('started')

channel.start_consuming()

channel.close()