from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QPropertyAnimation, QRect, QParallelAnimationGroup, QThread
# from PyQt5 import uic

from win_ui import Ui_MainWindow
from SenderThread import SenderThread

import sys
import configparser
import pika.exceptions


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.ui = uic.loadUi('untitled2.ui', self)
        self.connection = None
        self.channel = None
        self.queue_name = None
        self.client_id = 1
        self.sender_obj = None
        self.sender_thread = None
        try:
            self.load_conf()
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 'Error! conf.ini - file not found!', QMessageBox.Ok, QMessageBox.Ok)
            sys.exit(0)

        self.btn_connect.clicked.connect(self.connect_pika)
        self.btn_disconnect.clicked.connect(self.disconnect_pika)
        self.btn_send.clicked.connect(self.send_msg)
        self.btn_log.clicked.connect(self.show_log)

    def load_conf(self):
        config = configparser.ConfigParser()
        if config.read('conf.ini'):
            self.lineEdit_login.setText(config.get('Authentication', 'username', fallback='guest'))
            self.lineEdit_password.setText(config.get('Authentication', 'password', fallback='guest'))
            self.lineEdit_host.setText(config.get('Authentication', 'host', fallback='localhost'))
            self.lineEdit_port.setText(config.get('Authentication', 'port', fallback='5672'))
            # self.log_level = config.get('Logging', 'log_level', fallback='DEBUG')
            # self.log_file = config.get('Logging', 'log_file', fallback='app.log')
        else:
            raise FileNotFoundError

    def connect_pika(self):
        try:
            credentials = pika.PlainCredentials(self.lineEdit_login.text(), self.lineEdit_password.text())
            params = pika.ConnectionParameters(self.lineEdit_host.text(), self.lineEdit_port.text(),
                                               credentials=credentials)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='requests_queue')
            self.queue_name = self.channel.queue_declare(queue='', exclusive=True).method.queue
            self.show_frame(self.frame_sender, self.frame_connect)
            self.lineEdit_number.setText('0')
            self.make_consuming_thread()
        except pika.exceptions.AMQPConnectionError:
            QMessageBox.critical(self, 'Error', 'Error! Connect failed', QMessageBox.Ok, QMessageBox.Ok)

    def make_consuming_thread(self):
        self.sender_obj = SenderThread(self.channel, self.queue_name)
        self.sender_thread = QThread()
        self.sender_obj.moveToThread(self.sender_thread)
        self.sender_thread.started.connect(self.sender_obj.start)
        self.sender_obj.any_signal.connect(self.set_info)
        self.sender_thread.start()

    def send_msg(self):
        try:
            number = self.lineEdit_number.text()
            request = f'{self.client_id},{number}\n'
            self.channel.basic_publish(exchange='',
                                       routing_key='requests_queue',
                                       body=request,
                                       properties=pika.BasicProperties(reply_to=self.queue_name))
            self.textBrowser.append(f'Отправлено число {number}. Ждем ответ от сервера...')
        except Exception as e:
            print(f'{e}\nНеобработанная ошибка в send_msg')

    def disconnect_pika(self):
        self.show_frame(self.frame_connect, self.frame_sender)
        self.textBrowser.clear()
        try:
            self.connection.close()
        except pika.exceptions.StreamLostError as e:
            print(f'{e}\nЗадолбала')
        finally:
            self.sender_thread.terminate()
            self.sender_obj = None
            self.sender_thread = None
        # try:
        #     self.connection.close()
        #     self.textBrowser.clear()
        #     self.show_frame(self.frame_connect, self.frame_sender)
        #     if self.sender_thread:
        #         self.sender_thread.terminate()
        #         self.sender_obj = None
        #         self.sender_thread = None
        # except pika.exceptions.StreamLostError as e:
        #     print(f'{e}\nfrom client_ui')
        #     self.show_frame(self.frame_connect, self.frame_sender)
        #     if self.sender_thread:
        #         self.sender_thread.terminate()
        #         self.sender_obj = None
        #         self.sender_thread = None

    def show_frame(self, frame1, frame2):
        main_window_geometry = self.geometry()

        self.anim = QPropertyAnimation(frame1, b"geometry")
        self.anim.setDuration(500)
        self.anim.setStartValue(QRect(0, 0, main_window_geometry.width(), 0))
        self.anim.setEndValue(QRect(0, 0, main_window_geometry.width(), 200))

        self.anim_2 = QPropertyAnimation(frame2, b"geometry")
        self.anim_2.setDuration(500)
        self.anim_2.setEndValue(QRect(0, 200, main_window_geometry.width(), 0))

        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.anim)
        self.anim_group.addAnimation(self.anim_2)
        self.anim_group.start()

    def set_info(self, result):
        self.textBrowser.append(f"На число {result.decode('utf-8').split(',')[0]} "
                                f"получен ответ: {result.decode('utf-8').split(',')[1]}")

    def show_log(self):
        pass

    def closeEvent(self, a0):
        print("Closed app")
        if self.sender_thread:
            self.sender_thread.terminate()
        a0.accept()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
