# Form implementation generated from reading ui file 'settingsUI.ui'
#
# Created by: PyQt6 UI code generator 6.5.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(341, 350)
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(130, 130, 130);\n"
"\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QLabel{\n"
"    color: rgb(130, 130, 130);\n"
"}\n"
"\n"
"QLineEdit{\n"
"    background-color: rgb(40, 40, 40);\n"
"    color: rgb(130, 130, 130);\n"
"\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton{\n"
"    background-color: rgb(40, 40, 40);\n"
"    color: rgb(130, 130, 130);\n"
"\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(130, 130, 130);\n"
"    color: rgb(130, 130, 130);\n"
"\n"
"    border-radius: 5px;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbl_settings = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_settings.setGeometry(QtCore.QRect(10, 0, 211, 71))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.lbl_settings.setFont(font)
        self.lbl_settings.setObjectName("lbl_settings")
        self.le_clientIp = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.le_clientIp.setGeometry(QtCore.QRect(10, 140, 151, 21))
        self.le_clientIp.setObjectName("le_clientIp")
        self.le_clientPort = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.le_clientPort.setGeometry(QtCore.QRect(10, 190, 151, 21))
        self.le_clientPort.setObjectName("le_clientPort")
        self.btn_save = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(220, 310, 113, 32))
        self.btn_save.setObjectName("btn_save")
        self.lbl_clientIp = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_clientIp.setGeometry(QtCore.QRect(10, 120, 81, 16))
        self.lbl_clientIp.setObjectName("lbl_clientIp")
        self.lbl_clientPort = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_clientPort.setGeometry(QtCore.QRect(10, 170, 81, 16))
        self.lbl_clientPort.setObjectName("lbl_clientPort")
        self.le_serverIp = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.le_serverIp.setGeometry(QtCore.QRect(180, 140, 151, 21))
        self.le_serverIp.setObjectName("le_serverIp")
        self.lbl_serverIp = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_serverIp.setGeometry(QtCore.QRect(180, 120, 81, 16))
        self.lbl_serverIp.setObjectName("lbl_serverIp")
        self.lbl_serverPort = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_serverPort.setGeometry(QtCore.QRect(180, 170, 81, 16))
        self.lbl_serverPort.setObjectName("lbl_serverPort")
        self.le_serverPort = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.le_serverPort.setGeometry(QtCore.QRect(180, 190, 151, 21))
        self.le_serverPort.setObjectName("le_serverPort")
        self.lbl_client = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_client.setGeometry(QtCore.QRect(10, 75, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_client.setFont(font)
        self.lbl_client.setObjectName("lbl_client")
        self.lbl_server = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_server.setGeometry(QtCore.QRect(180, 70, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_server.setFont(font)
        self.lbl_server.setObjectName("lbl_server")
        self.le_path = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.le_path.setGeometry(QtCore.QRect(180, 240, 151, 21))
        self.le_path.setObjectName("le_path")
        self.lbl_path = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_path.setGeometry(QtCore.QRect(180, 220, 151, 16))
        self.lbl_path.setObjectName("lbl_path")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_settings.setText(_translate("MainWindow", "Settings"))
        self.btn_save.setText(_translate("MainWindow", "save"))
        self.lbl_clientIp.setText(_translate("MainWindow", "Server\'s ip"))
        self.lbl_clientPort.setText(_translate("MainWindow", "Server\'s port"))
        self.lbl_serverIp.setText(_translate("MainWindow", "ip"))
        self.lbl_serverPort.setText(_translate("MainWindow", "port"))
        self.lbl_client.setText(_translate("MainWindow", "client"))
        self.lbl_server.setText(_translate("MainWindow", "server"))
        self.lbl_path.setText(_translate("MainWindow", "path to save files"))
