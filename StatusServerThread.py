from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

import pika.exceptions


class StatusServerThread(QObject):
    start_status_server = pyqtSignal(tuple)
    server_online = pyqtSignal(bool)
    close_conn = pyqtSignal()

    def __init__(self, duration=5):
        super().__init__()
        self.start_status_server.connect(self.start_check) # noqa
        self.close_conn.connect(self.close_connection) # noqa
        self.connection = None
        self.channel = None
        self.duration = duration
        self.status_flag = True

    @pyqtSlot(tuple)
    def start_check(self, params_tuple):
        self.status_flag = True
        while self.status_flag:
            self.connect_pika(params_tuple)
            QThread.sleep(self.duration)

    def connect_pika(self, params_tuple):
        try:
            credentials = pika.PlainCredentials(params_tuple[0], params_tuple[1])
            params = pika.ConnectionParameters(params_tuple[2], params_tuple[3], credentials=credentials)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()

            # Попытка объявления очереди
            self.channel.queue_declare(queue='server_online', passive=True)

            # Если успешно, значит, очередь существует
            self.server_online.emit(True) # noqa
            return True
        except (pika.exceptions.ChannelClosed, pika.exceptions.AMQPConnectionError):
            # Обработка исключения, если канал закрыт (очереди не существует)
            self.server_online.emit(False) # noqa
            return False
        finally:
            # Закрытие соединения
            if self.connection and self.connection.is_open:
                self.connection.close()

    # @pyqtSlot()
    def close_connection(self):
        self.status_flag = False
        try:
            if self.channel and self.channel.is_open:
                self.channel.close()
                self.connection.close()
        except pika.exceptions.StreamLostError:
            print(__name__, 'Удаленный хост принудительно разорвал существующее подключение')
        self.connection = None
        self.channel = None
        print(__name__, 'close')
