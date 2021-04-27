import pika


def producer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            'localhost', 5672, credentials=pika.PlainCredentials('guest', 'guest')
        ))

    channel = connection.channel()

    channel.queue_declare('hello')

    channel.basic_publish('', 'hello', 'This is the first message')
    channel.close()


def consumer():

    def on_message_callback(channel, method, properties, body):
        print(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            'localhost', 5672, credentials=pika.PlainCredentials('guest', 'guest')
        ))

    channel = connection.channel()

    channel.queue_declare('hello')

    # channel.basic_qos(prefetch_count=1) # 类似权重, 按能力分发, 如果有一条消息, 就不在给你发
    channel.basic_consume('hello', on_message_callback)

    # for method, properties, body in channel.consume('hello'):
    #     print(body)
    #     channel.basic_ack(delivery_tag=method.delivery_tag)

    print("[*]Waiting for message. To exit press CTRL+C")
    channel.start_consuming()
