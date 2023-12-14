import pika
import time
import random

def callback(ch, method, properties, body):
    # Получаем данные из запроса
    request_data = body.decode('utf-8')
    client_id, number = map(int, request_data.split(','))

    # Обрабатываем запрос: умножаем число на 2
    result = number * 2
    print(f'From ID: {client_id} received: {number} sent back: {result}.')
    time.sleep(random.randint(3, 9))

    # Отправляем ответ в уникальную очередь ответов для данного клиента
    response_queue_name = f'response_queue_{client_id}'

    ch.basic_publish(exchange='', routing_key=response_queue_name, body=str(result))


# Устанавливаем соединение
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_exchange')
channel.queue_declare(queue='requests_queue')
channel.queue_bind(exchange='direct_exchange', queue='requests_queue')

# Устанавливаем callback-функцию для обработки запросов
channel.basic_consume(queue='requests_queue', on_message_callback=callback, auto_ack=True)

print('Ожидание запросов. Для выхода нажмите CTRL+C')
channel.start_consuming()
