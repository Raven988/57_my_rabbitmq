import pika.exceptions
import sys
import configparser
import logging


class Client:
    def __init__(self, client_id):
        self.client_id = client_id
        self.credentials = None
        self.connection = None
        self.channel = None
        self.result = None
        self.queue_name = None
        self.logger = None
        self.username = None
        self.password = None
        self.host = None
        self.port = None
        self.log_level = None
        self.log_file = None
        self.load_conf()
        self.connect()
        self.start()

    def load_conf(self):
        config = configparser.ConfigParser()
        if config.read('conf.ini'):
            self.username = config.get('Authentication', 'username', fallback='guest')
            self.password = config.get('Authentication', 'password', fallback='guest')
            self.host = config.get('Authentication', 'host', fallback='localhost')
            self.port = config.get('Authentication', 'port', fallback='5672')
            self.log_level = config.get('Logging', 'log_level', fallback='DEBUG')
            self.log_file = config.get('Logging', 'log_file', fallback='app.log')
        else:
            raise FileNotFoundError

    def set_logger(self, log_level, log_file):
        file_handler = logging.FileHandler(filename=log_file, mode='a')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger = logging.getLogger('logger')
        self.logger.setLevel(log_level)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def connect(self):
        try:
            self.credentials = pika.PlainCredentials(username=self.username, password=self.password)
            conn_params = pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.credentials)
            self.connection = pika.BlockingConnection(conn_params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='requests_queue')
            self.result = self.channel.queue_declare(queue='', exclusive=True)
            self.queue_name = self.result.method.queue
        except pika.exceptions.AMQPConnectionError:
            print('Ошибка соединения')
            exit(0)

    def start(self):
        try:
            while True:
                self.send_request()
                self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
                self.channel.start_consuming()
        except KeyboardInterrupt:
            print('\nВыход')
            exit(0)

    def send_request(self):
        number = input('Input number: ')
        if not number:
            number = 0
        request_data = f'{self.client_id},{number}'
        self.channel.basic_publish(exchange='',
                                   routing_key='requests_queue',
                                   body=request_data,
                                   properties=pika.BasicProperties(reply_to=self.queue_name))
        print(f"Отправлен запрос от клиента {self.client_id} для числа {number}")

    def callback(self, ch, method, properties, body):
        print(f"Получен ответ для клиента {self.client_id}: {body.decode('utf-8')}")
        self.channel.stop_consuming()


if __name__ == '__main__':
    client1 = Client(1)
