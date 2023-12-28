import threading

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QPropertyAnimation, QRect, QParallelAnimationGroup, QThread, pyqtSlot
# from PyQt5 import uic

from win_ui import Ui_MainWindow
from SenderThread import SenderThread

import sys
import configparser
import threading
import pika.exceptions
import os


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        print(f'Main Thread: {threading.get_native_id()}')
        self.setupUi(self)
        # self.ui = uic.loadUi('untitled2.ui', self)
        self.queue_name = None
        self.client_id = 1
        self.pika_obj = None
        self.pika_thread = None
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
        self.pika_thread = QThread()
        self.pika_obj = SenderThread(self.lineEdit_login.text(),
                                     self.lineEdit_password.text(),
                                     self.lineEdit_host.text(),
                                     self.lineEdit_port.text())
        self.pika_obj.moveToThread(self.pika_thread)
        self.pika_obj.signal_response.connect(self.set_info)
        self.pika_obj.connection_close.connect(self.connection_close)
        self.pika_thread.started.connect(self.pika_obj.start) # noqa
        self.pika_thread.start()

    def connection_close(self, result):
        if not result:
            self.lineEdit_number.setText('0')
            self.show_frame(self.frame_sender, self.frame_connect)
        else:
            QMessageBox.critical(self, 'Error', 'ConnectionError!', QMessageBox.Ok, QMessageBox.Ok)
            self.pika_thread.quit()

    def send_msg(self):
        number = self.lineEdit_number.text()
        request = f'{self.client_id},{number}\n'
        self.textBrowser.append(f'Отправлено число {number}. Ждем ответ от сервера...')
        self.pika_obj.request_from_main.emit(request)

    def disconnect_pika(self):
        # # Закрываем текущий цикл обработки событий
        # qApp = QApplication.instance()
        # qApp.quit()
        # # Перезапускаем программу
        # python = sys.executable
        # os.execl(python, python, *sys.argv)
        self.show_frame(self.frame_connect, self.frame_sender)
        self.textBrowser.clear()
        if self.pika_thread:
            self.pika_obj.close_conn.emit()
            self.pika_thread.quit()
            # self.pika_thread = None
            print('disconnect_pika')

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
        self.disconnect_pika()
        if self.pika_thread:
            self.pika_thread.quit()
            print("thread stopped")
        a0.accept()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
