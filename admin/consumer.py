import json
import pika
import django, os

os.environ['DJANGO_SETTINGS_MODULE'] = 'admin.settings'
django.setup()

from products.models import Product

params = pika.URLParameters('amqps://wqcqaqin:GL8aGVdApoUXWnl7NrCqojT-4rUauyQZ@jackal.rmq.cloudamqp.com/wqcqaqin')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(" [x] Received in Admin %r" % data)

    if properties.content_type == 'product_liked':
        product = Product.objects.get(id=data)
        product.likes = product.likes + 1
        product.save()
        print('Product {} liked'.format(data))

channel.basic_consume(queue='admin', auto_ack=True, on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()

# channel.close()