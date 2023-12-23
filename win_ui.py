# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\untitled2.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(570, 240)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(570, 240))
        MainWindow.setMaximumSize(QtCore.QSize(570, 240))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_sender = QtWidgets.QFrame(self.centralwidget)
        self.frame_sender.setGeometry(QtCore.QRect(0, 0, 560, 0))
        self.frame_sender.setStyleSheet("")
        self.frame_sender.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_sender.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sender.setLineWidth(1)
        self.frame_sender.setObjectName("frame_sender")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_sender)
        self.gridLayout.setObjectName("gridLayout")
        self.label_input = QtWidgets.QLabel(self.frame_sender)
        self.label_input.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_input.setFont(font)
        self.label_input.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_input.setObjectName("label_input")
        self.gridLayout.addWidget(self.label_input, 1, 0, 1, 1)
        self.lineEdit_number = QtWidgets.QLineEdit(self.frame_sender)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_number.setFont(font)
        self.lineEdit_number.setObjectName("lineEdit_number")
        self.gridLayout.addWidget(self.lineEdit_number, 2, 0, 1, 1)
        self.btn_log = QtWidgets.QPushButton(self.frame_sender)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_log.setFont(font)
        self.btn_log.setObjectName("btn_log")
        self.gridLayout.addWidget(self.btn_log, 4, 0, 1, 1)
        self.btn_send = QtWidgets.QPushButton(self.frame_sender)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_send.setFont(font)
        self.btn_send.setObjectName("btn_send")
        self.gridLayout.addWidget(self.btn_send, 3, 0, 1, 1)
        self.btn_disconnect = QtWidgets.QPushButton(self.frame_sender)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.btn_disconnect.setFont(font)
        self.btn_disconnect.setObjectName("btn_disconnect")
        self.gridLayout.addWidget(self.btn_disconnect, 5, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.frame_sender)
        self.textBrowser.setMinimumSize(QtCore.QSize(400, 200))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 1, 5, 1)
        self.frame_connect = QtWidgets.QFrame(self.centralwidget)
        self.frame_connect.setGeometry(QtCore.QRect(0, 0, 560, 200))
        self.frame_connect.setStyleSheet("")
        self.frame_connect.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_connect.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_connect.setObjectName("frame_connect")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_connect)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_login = QtWidgets.QLabel(self.frame_connect)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_login.setFont(font)
        self.label_login.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_login.setObjectName("label_login")
        self.gridLayout_2.addWidget(self.label_login, 0, 0, 1, 1)
        self.lineEdit_login = QtWidgets.QLineEdit(self.frame_connect)
        self.lineEdit_login.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_login.setFont(font)
        self.lineEdit_login.setStyleSheet("")
        self.lineEdit_login.setObjectName("lineEdit_login")
        self.gridLayout_2.addWidget(self.lineEdit_login, 0, 1, 1, 1)
        self.label_password = QtWidgets.QLabel(self.frame_connect)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_password.setFont(font)
        self.label_password.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_password.setObjectName("label_password")
        self.gridLayout_2.addWidget(self.label_password, 1, 0, 1, 1)
        self.lineEdit_password = QtWidgets.QLineEdit(self.frame_connect)
        self.lineEdit_password.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_password.setFont(font)
        self.lineEdit_password.setStyleSheet("")
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.gridLayout_2.addWidget(self.lineEdit_password, 1, 1, 1, 1)
        self.label_host = QtWidgets.QLabel(self.frame_connect)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_host.setFont(font)
        self.label_host.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_host.setObjectName("label_host")
        self.gridLayout_2.addWidget(self.label_host, 2, 0, 1, 1)
        self.lineEdit_host = QtWidgets.QLineEdit(self.frame_connect)
        self.lineEdit_host.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_host.setFont(font)
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.gridLayout_2.addWidget(self.lineEdit_host, 2, 1, 1, 1)
        self.label_port = QtWidgets.QLabel(self.frame_connect)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_port.setFont(font)
        self.label_port.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_port.setObjectName("label_port")
        self.gridLayout_2.addWidget(self.label_port, 3, 0, 1, 1)
        self.lineEdit_port = QtWidgets.QLineEdit(self.frame_connect)
        self.lineEdit_port.setMaximumSize(QtCore.QSize(350, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_port.setFont(font)
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.gridLayout_2.addWidget(self.lineEdit_port, 3, 1, 1, 1)
        self.btn_connect = QtWidgets.QPushButton(self.frame_connect)
        self.btn_connect.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_connect.setFont(font)
        self.btn_connect.setAutoFillBackground(False)
        self.btn_connect.setCheckable(False)
        self.btn_connect.setAutoRepeat(False)
        self.btn_connect.setObjectName("btn_connect")
        self.gridLayout_2.addWidget(self.btn_connect, 4, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_input.setText(_translate("MainWindow", "Input number"))
        self.btn_log.setText(_translate("MainWindow", "Log"))
        self.btn_send.setText(_translate("MainWindow", "Send"))
        self.btn_disconnect.setText(_translate("MainWindow", "Disconnect"))
        self.label_login.setText(_translate("MainWindow", "Login"))
        self.label_password.setText(_translate("MainWindow", "Password"))
        self.label_host.setText(_translate("MainWindow", "Host"))
        self.label_port.setText(_translate("MainWindow", "Port"))
        self.btn_connect.setText(_translate("MainWindow", "Connect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())