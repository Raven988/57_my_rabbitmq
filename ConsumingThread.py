from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
import pika.exceptions


class ConsumingThread(QObject):
    connection_close = pyqtSignal()
    close_conn = pyqtSignal()
    signal_response = pyqtSignal(bytes)
    exclusive_queue = pyqtSignal(str)
    ready_to_connect = pyqtSignal(bool)
    conn_params = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.connection_close.connect(self.stop_cons) # noqa
        self.close_conn.connect(self.close_connection) # noqa
        self.conn_params.connect(self.connect_pika) # noqa
        self.connection = None
        self.channel = None
        self.queue_name = None
        self.stop_flag = False

    # @pyqtSlot()
    def stop_cons(self):
        if self.channel and self.connection.is_open:
            QThread.sleep(1)
            self.channel.stop_consuming()

    @pyqtSlot(tuple)
    def connect_pika(self, params_tuple):
        try:
            credentials = pika.PlainCredentials(params_tuple[0], params_tuple[1])
            params = pika.ConnectionParameters(params_tuple[2], params_tuple[3], credentials=credentials)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='requests_queue')
            self.queue_name = self.channel.queue_declare(queue='', exclusive=True).method.queue
            self.exclusive_queue.emit(self.queue_name) # noqa
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            self.channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            self.connection = None
            self.channel = None
            self.ready_to_connect.emit(False) # noqa
            print(__name__, 'Удаленный хост принудительно разорвал существующее подключение')

    def callback(self, ch, method, properties, body):  # noqa
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

