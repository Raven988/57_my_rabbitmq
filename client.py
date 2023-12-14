import pika
import time
import sys
import random

class Client:
    def __init__(self, client_id):
        self.client_id = client_id
        # self.response_queue_name = f'response_queue_{client_id}'
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='direct_exchange')
        self.channel.queue_declare(queue='requests_queue')
        self.channel.queue_bind(exchange='direct_exchange', queue='requests_queue')

        # Создаем уникальную очередь ответов для данного клиента
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue

        while True:
            self.send_request()

            # Устанавливаем callback-функцию для обработки ответов
            self.channel.basic_consume(queue=self.queue_name,
                                       on_message_callback=self.callback,
                                       auto_ack=True)
            self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(f"Получен ответ для клиента {self.client_id}: {body.decode('utf-8')}")
        self.channel.stop_consuming()

    def send_request(self):
        number = input('Input number: ')
        # Отправляем запрос в общую очередь запросов
        request_data = f"{self.client_id},{number}"
        self.channel.basic_publish(exchange='direct_exchange',
                                   routing_key='requests_queue',
                                   body=request_data,
                                   properties=pika.BasicProperties(reply_to=self.queue_name))

        # Ожидаем ответа
        print(f"Отправлен запрос от клиента {self.client_id} для числа {number}")
        time.sleep(random.randint(3, 9))


client1 = Client(client_id=sys.argv[1])
