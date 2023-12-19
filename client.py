import pika.exceptions
import sys
import configparser


class Client:
    def __init__(self, client_id):
        self.client_id = client_id
        self.credentials = None
        self.connection = None
        self.channel = None
        self.result = None
        self.queue_name = None
        self.connect()
        self.start()

    def connect(self):
        config = configparser.ConfigParser()
        if config.read('config.ini'):
            username = config.get('Authentication', 'username', fallback='guest')
            password = config.get('Authentication', 'password', fallback='guest')
            host = config.get('Authentication', 'host', fallback='localhost')
            port = config.get('Authentication', 'port', fallback='5672')
        else:
            print('Конфигурационный файл не обнаружен')
            exit(0)

        try:
            self.credentials = pika.PlainCredentials(username=username, password=password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port,
                                                                                credentials=self.credentials))
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
        request_data = f'{self.client_id},{number}'
        self.channel.basic_publish(exchange='',
                                   routing_key='requests_queue',
                                   body=request_data,
                                   properties=pika.BasicProperties(reply_to=self.queue_name))
        print(f"Отправлен запрос от клиента {self.client_id} для числа {number}")

    def callback(self, ch, method, properties, body):
        print(f"Получен ответ для клиента {self.client_id}: {body.decode('utf-8')}")
        self.channel.stop_consuming()


client1 = Client(client_id=sys.argv[1])
