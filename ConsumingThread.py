from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
import pika.exceptions
import threading


class ConsumingThread(QObject):
    connection_close = pyqtSignal()
    start_consumer = pyqtSignal()
    close_conn = pyqtSignal()
    signal_response = pyqtSignal(bytes)
    exclusive_queue = pyqtSignal(str)
    ready_to_connect = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.connection_close.connect(self.test) # noqa
        self.start_consumer.connect(self.consumer) # noqa
        self.close_conn.connect(self.close_connection) # noqa
        self.connection = None
        self.channel = None
        self.queue_name = None
        self.stop_flag = False

    # @pyqtSlot()
    def test(self):
        if self.channel and self.connection.is_open:
            QThread.sleep(1)
            self.channel.stop_consuming()

    def connect_pika(self, params):
        try:
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='requests_queue')
            self.queue_name = self.channel.queue_declare(queue='', exclusive=True).method.queue
            self.exclusive_queue.emit(self.queue_name) # noqa
        except pika.exceptions.AMQPConnectionError:
            pass

    @pyqtSlot()
    def consumer(self):
        QThread.sleep(1)
        try:
            if self.channel:
                self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
                self.channel.start_consuming()
        except pika.exceptions.StreamLostError:
            self.connection = None
            self.channel = None
            self.ready_to_connect.emit(False) # noqa
            print(__name__, 'Удаленный хост принудительно разорвал существующее подключение')

    def callback(self, ch, method, properties, body):  # noqa
        if body == 'stop consuming':
            self.channel.stop_consuming()
            return
        self.signal_response.emit(body)  # noqa

    @pyqtSlot()
    def close_connection(self):
        if self.connection and self.connection.is_open:
            self.channel.close()
            self.connection.close()
        self.connection = None
        self.channel = None
        self.ready_to_connect.emit(True) # noqa
        print(__name__, 'cons close')

