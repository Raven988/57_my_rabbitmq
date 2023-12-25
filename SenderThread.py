from PyQt5.QtCore import QObject, pyqtSignal
import pika.exceptions


class SenderThread(QObject):
    any_signal = pyqtSignal(bytes)
    def __init__(self, chanel, queue):
        super(SenderThread, self).__init__()
        self.channel = chanel
        self.queue = queue

    def start(self):
        try:
            self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
            self.channel.start_consuming()
        except pika.exceptions.StreamLostError as e:
            print(f'{e}\nfrom sender')

    def callback(self, ch, method, properties, body):
        self.any_signal.emit(body)
