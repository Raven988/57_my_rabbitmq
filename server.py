import pika.exceptions
import configparser
import logging
import sys
import time


config = configparser.ConfigParser()
if config.read('conf.ini'):
    username = config.get('Authentication', 'username', fallback='guest')
    password = config.get('Authentication', 'password', fallback='guest')
    host = config.get('Authentication', 'host', fallback='localhost')
    port = config.get('Authentication', 'port', fallback='5672')
    log_level = config.get('Logging', 'log_level', fallback='DEBUG')
    log_file = config.get('Logging', 'log_file', fallback='app.log')
else:
    raise FileNotFoundError


file_handler = logging.FileHandler(filename=log_file, mode='a')
file_handler.setLevel(log_level)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(message)s'))
logger = logging.getLogger('logger')
logger.setLevel(log_level)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def callback(ch, method, properties, body):
    request_data = body.decode('utf-8')
    client_id, number = map(int, request_data.split(','))
    result = f'{number},{number * 2}'
    logger.debug(f'Имя очереди: {properties.reply_to}')
    logger.info(f'Получено число {number} от клиента {client_id}. Отправлено {number * 2}')
    time.sleep(6)
    ch.basic_publish(exchange='', routing_key=properties.reply_to, body=result)



logger.debug(f'Подключение к серверу...\nUsername -> {username}\nHost -> {host}:{port}')
credentials = pika.PlainCredentials(username=username, password=password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=credentials))
channel = connection.channel()
try:
    channel.queue_declare(queue='server_online')
    channel.queue_declare(queue='requests_queue')
    channel.basic_consume(queue='requests_queue', on_message_callback=callback, auto_ack=True)
    logger.info('Ожидание запросов. Для выхода нажмите CTRL+C')
    channel.start_consuming()
except pika.exceptions.AMQPConnectionError:
    channel.queue_delete(queue='server_online')
    logger.error('Ошибка соединения')
except KeyboardInterrupt:
    channel.queue_delete(queue='server_online')
    logger.info('Exit')
