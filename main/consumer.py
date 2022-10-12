from app import Product, db
import pika, json

params = pika.URLParameters('amqps://wqcqaqin:GL8aGVdApoUXWnl7NrCqojT-4rUauyQZ@jackal.rmq.cloudamqp.com/wqcqaqin')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    # print(" [x] Received in Main %r" % body)
    data = json.loads(body)
    print(" [x] Received Main %r" % data)
    print(properties.content_type)
    
    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title= data['title'], image = data['image'])
        db.session.add(product)
        db.session.commit()
        print(" [x] Product Created %r" % product.id)
        
    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data.title
        product.image = data.image
        db.session.commit()
        print(" [x] Product Updated %r" % product.id)
                
    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data['id'])
        db.session.delete()
        db.session.commit()
        print(" [x] Product Deleted %r" % product.id)
        

channel.basic_consume(queue='main', auto_ack=True, on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()

# channel.close()