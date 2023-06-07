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
        MainWindow.resize(280, 250)
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
        self.lbl_settings.setGeometry(QtCore.QRect(10, 10, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.lbl_settings.setFont(font)
        self.lbl_settings.setObjectName("lbl_settings")
        self.le_ip = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.le_ip.setGeometry(QtCore.QRect(10, 110, 151, 21))
        self.le_ip.setObjectName("le_ip")
        self.le_port = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.le_port.setGeometry(QtCore.QRect(10, 160, 151, 21))
        self.le_port.setObjectName("le_port")
        self.btn_save = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(160, 210, 113, 32))
        self.btn_save.setObjectName("btn_save")
        self.lbl_ip = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_ip.setGeometry(QtCore.QRect(10, 90, 81, 16))
        self.lbl_ip.setObjectName("lbl_ip")
        self.lbl_port = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_port.setGeometry(QtCore.QRect(10, 140, 81, 16))
        self.lbl_port.setObjectName("lbl_port")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_settings.setText(_translate("MainWindow", "Settings"))
        self.btn_save.setText(_translate("MainWindow", "save"))
        self.lbl_ip.setText(_translate("MainWindow", "Server\'s ip"))
        self.lbl_port.setText(_translate("MainWindow", "Server\'s port"))
