from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
import pika.exceptions
import threading


class SenderThread(QObject):
    # my_signal = pyqtSignal()
    request_from_main = pyqtSignal(str)
    signal_response = pyqtSignal(bytes)
    close_conn = pyqtSignal()
    connection_close = pyqtSignal(bool)

    def __init__(self, login, pwd, host, port):
        super(SenderThread, self).__init__()
        # self.my_signal.connect(self.show_IdThread)
        self.request_from_main.connect(self.request)
        self.close_conn.connect(self.close_connection)
        self.login = login
        self.pwd = pwd
        self.host = host
        self.port = port
        self.connection = None
        self.channel = None
        self.queue_name = None

    # @pyqtSlot()
    # def show_IdThread(self):
    #     print(f'Worker Thread: {threading.current_thread().ident}')

    # @pyqtSlot()
    def start(self):
        print(f'thread id {threading.get_native_id()}')
        try:
            credentials = pika.PlainCredentials(self.login, self.pwd)
            params = pika.ConnectionParameters(self.host, self.port, credentials=credentials)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='requests_queue')
            self.queue_name = self.channel.queue_declare(queue='', exclusive=True).method.queue
            self.connection_close.emit(False) # noqa
        except pika.exceptions.AMQPConnectionError:
            self.connection_close.emit(True) # noqa
            print(f'ConnectionError')

    @pyqtSlot(str)
    def request(self, request):
        try:
            self.channel.basic_publish(exchange='',
                                       routing_key='requests_queue',
                                       body=request,
                                       properties=pika.BasicProperties(reply_to=self.queue_name))
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            self.channel.start_consuming()
        except pika.exceptions.AMQPError as e:
            print(f'{e}\n2error from SenderThread.py def from_main')
        except Exception as e:
            print(f'{e}\n1error from SenderThread.py def from_main')

    # @pyqtSlot()
    def callback(self, ch, method, properties, body): # noqa
        self.channel.stop_consuming()
        self.signal_response.emit(body) # noqa

    @pyqtSlot()
    def close_connection(self):
        # try:
        if self.connection and self.connection.is_open:
            self.channel.stop_consuming()
            self.channel.close()
            self.connection.close()
        # except pika.exceptions.AMQPError as e:
        #     print(f'{e}\n1error from SenderThread.py def close_connect')
        # except Exception as e:
        #     print(f'{e}\n2error from SenderThread.py def close_connect')
