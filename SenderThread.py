from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import pika.exceptions
import threading

class SenderThread(QObject):
    signal_3 = pyqtSignal()
    signal_from_main = pyqtSignal(str)
    any_signal = pyqtSignal(bytes)
    close = pyqtSignal()
    test_signal1 = pyqtSignal()
    def __init__(self, login, pwd, host, port):
        super(SenderThread, self).__init__()
        print(f'from init {threading.get_native_id()}')
        self.signal_3.connect(self.signal3_from_Main)
        self.signal_from_main.connect(self.from_main)
        self.close.connect(self.close_connect)
        self.test_signal1.connect(self.test_signal)
        self.login = login
        self.pwd = pwd
        self.host = host
        self.port = port
        self.connection = None
        self.channel = None
        self.queue_name = None

    def reply_con(self):
        self.channel.start_consuming()

    @pyqtSlot()
    def signal3_from_Main(self):
        print(threading.current_thread().ident)

    @pyqtSlot()
    def test_signal(self):
        print(f'from test {threading.get_native_id()}')

    # @pyqtSlot()
    def start(self):
        print(f'from start {threading.get_native_id()}')
        try:
            credentials = pika.PlainCredentials(self.login, self.pwd)
            params = pika.ConnectionParameters(self.host, self.port, credentials=credentials)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='requests_queue')
            self.queue_name = self.channel.queue_declare(queue='', exclusive=True).method.queue
            # self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
            # self.channel.start_consuming()
        except Exception as e:
            print(f'{e}\nfrom start')

    @pyqtSlot(str)
    def from_main(self, request):
        print(f'from from_main {threading.get_native_id()}')
        self.channel.basic_publish(exchange='',
                                   routing_key='requests_queue',
                                   body=request,
                                   properties=pika.BasicProperties(reply_to=self.queue_name))
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    # @pyqtSlot()
    def callback(self, ch, method, properties, body):
        print(f'from callback {threading.get_native_id()}')
        self.channel.stop_consuming()
        self.any_signal.emit(body)

    @pyqtSlot()
    def close_connect(self):
        print(f'from close_conn {threading.get_native_id()}')
        self.connection.close()
