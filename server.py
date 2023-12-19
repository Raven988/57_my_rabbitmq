import pika.exceptions
import configparser


def callback(ch, method, properties, body):
    request_data = body.decode('utf-8')
    client_id, number = map(int, request_data.split(','))
    result = number * 2
    print(f'Queue name: {properties.reply_to}')
    print(f'From ID: {client_id} received: {number} sent back: {result}.')
    ch.basic_publish(exchange='', routing_key=properties.reply_to, body=str(result))


config = configparser.ConfigParser()
if config.read('config1.ini'):
    username = config.get('Authentication', 'username', fallback='guest')
    password = config.get('Authentication', 'password', fallback='guest')
    host = config.get('Authentication', 'host', fallback='localhost')
    port = config.get('Authentication', 'port', fallback='5672')
else:
    print('Конфигурационный файл не обнаружен')
    exit(0)


try:
    credentials = pika.PlainCredentials(username=username, password=password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='requests_queue')
    channel.basic_consume(queue='requests_queue', on_message_callback=callback, auto_ack=True)
    print('Ожидание запросов. Для выхода нажмите CTRL+C')
    channel.start_consuming()
except pika.exceptions.AMQPConnectionError:
    print('Ошибка соединения')
except KeyboardInterrupt:
    print('выход')
