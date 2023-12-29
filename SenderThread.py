from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
import pika.exceptions
import threading


class SenderThread(QObject):
    request_from_main = pyqtSignal(str, str)
    connection_close = pyqtSignal(bool)
    close_conn = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.request_from_main.connect(self.request) # noqa
        self.close_conn.connect(self.close_connection) # noqa
        self.connection = None
        self.channel = None
        self.queue_name = None

    def connect_pika(self, params):
        try:
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='requests_queue')
            self.connection_close.emit(False) # noqa
        except pika.exceptions.AMQPConnectionError:
            self.connection_close.emit(True) # noqa

    @pyqtSlot(str, str)
    def request(self, request, queue):
        try:
            self.channel.basic_publish(exchange='', routing_key='requests_queue', body=request,
                                       properties=pika.BasicProperties(reply_to=queue))
        except pika.exceptions.AMQPError as e:
            print(f'{e}\nerror from SenderThread.py def request')

    @pyqtSlot()
    def close_connection(self):
        try:
            if self.connection:
                self.channel.close()
                self.connection.close()
        except pika.exceptions.StreamLostError:
            print(__name__, 'Удаленный хост принудительно разорвал существующее подключение')
        self.connection = None
        self.channel = None
        print(__name__, 'sender close')
