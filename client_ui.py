from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QPropertyAnimation, QRect, QParallelAnimationGroup, QPoint, QEasingCurve

from win_ui import Ui_MainWindow
import sys
import configparser
import pika.exceptions


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = None
        self.channel = None
        self.queue_name = None
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
            conn_params = pika.ConnectionParameters(self.lineEdit_host.text(), self.lineEdit_port.text(),
                                                    credentials=credentials)
            self.connection = pika.BlockingConnection(conn_params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='requests_queue')
            result = self.channel.queue_declare(queue='', exclusive=True)
            self.queue_name = result.method.queue
            self.show_frame(self.frame_sender, self.frame_connect)
        except pika.exceptions.AMQPConnectionError:
            QMessageBox.critical(self, 'Error', 'Error! Connect failed', QMessageBox.Ok, QMessageBox.Ok)

    def disconnect_pika(self):
        try:
            self.connection.close()
            self.channel.close()
            self.show_frame(self.frame_connect, self.frame_sender)
        except pika.exceptions.ChannelWrongStateError:
            self.show_frame(self.frame_connect, self.frame_sender)

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

    def send_msg(self):
        pass

    def show_log(self):
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
