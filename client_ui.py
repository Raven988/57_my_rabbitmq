import threading

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QPropertyAnimation, QRect, QParallelAnimationGroup, QThread, pyqtSlot
# from PyQt5 import uic

from win_ui import Ui_MainWindow
from SenderThread import SenderThread
from ConsumingThread import ConsumingThread

import sys
import configparser
import threading
import pika.exceptions
import os

# class Window(QMainWindow):
class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        print(f'Main Thread: {threading.get_native_id()}')
        self.setupUi(self)
        # self.ui = uic.loadUi('untitled2.ui', self)
        self.exclusive_queue = None
        self.client_id = 1
        self.sender_obj = None
        self.sender_thread = None
        self.consuming_obj = None
        self.consuming_thread = None
        try:
            self.load_conf()
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 'Error! conf.ini - file not found!', QMessageBox.Ok, QMessageBox.Ok)
            sys.exit(0)

        self.make_threads()
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

    def make_threads(self):
        self.sender_thread = QThread()
        self.sender_obj = SenderThread()
        self.sender_obj.moveToThread(self.sender_thread)
        self.sender_obj.connection_close.connect(self.connection_close)
        self.sender_thread.start()

        self.consuming_thread = QThread()
        self.consuming_obj = ConsumingThread()
        self.consuming_obj.moveToThread(self.consuming_thread)
        self.consuming_obj.signal_response.connect(self.set_info)
        self.consuming_obj.exclusive_queue.connect(self.name_queue)
        self.consuming_obj.ready_to_connect.connect(self.open_button)
        self.consuming_thread.start()

    def open_button(self, result):
        if result:
            self.statusBar.showMessage('Готово', 2000)
            self.btn_connect.setText('Connect')
            self.btn_connect.setEnabled(True)
        else:
            self.disconnect_pika()

    def name_queue(self, queue):
        self.exclusive_queue = queue

    def connect_pika(self):
        self.btn_disconnect.setEnabled(True)
        self.btn_send.setEnabled(True)
        self.btn_log.setEnabled(True)
        credentials = pika.PlainCredentials(self.lineEdit_login.text(), self.lineEdit_password.text())
        params = pika.ConnectionParameters(self.lineEdit_host.text(), self.lineEdit_port.text(), credentials=credentials)
        self.sender_obj.connect_pika(params)
        self.consuming_obj.connect_pika(params)

    def connection_close(self, result):
        if not result:
            self.textBrowser.clear()
            self.lineEdit_number.setText('0')
            self.show_frame(self.frame_sender, self.frame_connect)
            self.consuming_obj.start_consumer.emit()
        else:
            QMessageBox.critical(self, 'Error', 'ConnectionError!', QMessageBox.Ok, QMessageBox.Ok)

    def send_msg(self):
        number = self.lineEdit_number.text()
        request = f'{self.client_id},{number}\n'
        self.textBrowser.append(f'Отправлено число {number}. Ждем ответ от сервера...')
        self.sender_obj.request_from_main.emit(request, self.exclusive_queue)

    def disconnect_pika(self):
        self.statusBar.showMessage('Выполняется отключение...')
        self.btn_connect.setEnabled(False)
        self.btn_connect.setText('Waiting...')
        self.btn_disconnect.setEnabled(False)
        self.btn_send.setEnabled(False)
        self.btn_log.setEnabled(False)
        self.show_frame(self.frame_connect, self.frame_sender)
        self.consuming_obj.connection_close.emit()
        self.consuming_obj.close_conn.emit()
        self.sender_obj.close_conn.emit()


    def show_frame(self, frame1, frame2):
        main_window_geometry = self.geometry()

        self.anim = QPropertyAnimation(frame1, b"geometry")
        self.anim.setDuration(500)
        self.anim.setStartValue(QRect(0, 0, main_window_geometry.width(), 0))
        self.anim.setEndValue(QRect(0, 0, main_window_geometry.width(), 220))

        self.anim_2 = QPropertyAnimation(frame2, b"geometry")
        self.anim_2.setDuration(500)
        self.anim_2.setEndValue(QRect(0, 220, main_window_geometry.width(), 0))

        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.anim)
        self.anim_group.addAnimation(self.anim_2)
        self.anim_group.start()

    def set_info(self, result):
        self.textBrowser.append(f"На число {result.decode('utf-8').split(',')[0]} "
                                f"получен ответ: {result.decode('utf-8').split(',')[1]}")

    def show_log(self):
        self.consuming_obj.connection_close.emit()

    def closeEvent(self, a0):
        print("Closed app")
        self.disconnect_pika()
        if self.sender_thread and self.consuming_thread:
            self.sender_thread.quit()
            self.sender_thread.wait()
            self.consuming_thread.quit()
            self.consuming_thread.wait()
            print("thread stopped")
        a0.accept()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
