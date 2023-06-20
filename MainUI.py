# Form implementation generated from reading ui file 'MainUI.ui'
#
# Created by: PyQt6 UI code generator 6.5.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(913, 310)
        font = QtGui.QFont()
        font.setFamily("Mona-Sans Regular")
        font.setPointSize(22)
        font.setItalic(True)
        MainWindow.setFont(font)
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
"QListView{\n"
"    background-color: rgb(40, 40, 40);\n"
"    color: rgb(130, 130, 130);\n"
"\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QProgressBar{\n"
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
        self.btn_send = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_send.setGeometry(QtCore.QRect(310, 260, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.btn_send.setFont(font)
        self.btn_send.setObjectName("btn_send")
        self.pb_progress = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.pb_progress.setGeometry(QtCore.QRect(0, 290, 451, 21))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pb_progress.setFont(font)
        self.pb_progress.setProperty("value", 24)
        self.pb_progress.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.pb_progress.setTextVisible(True)
        self.pb_progress.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.pb_progress.setInvertedAppearance(False)
        self.pb_progress.setObjectName("pb_progress")
        self.lbl_pic = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_pic.setGeometry(QtCore.QRect(100, 10, 251, 241))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lbl_pic.setFont(font)
        self.lbl_pic.setText("")
        self.lbl_pic.setPixmap(QtGui.QPixmap("assets/files.png"))
        self.lbl_pic.setScaledContents(True)
        self.lbl_pic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_pic.setObjectName("lbl_pic")
        self.lw_files_to = QtWidgets.QListWidget(parent=self.centralwidget)
        self.lw_files_to.setGeometry(QtCore.QRect(470, 10, 431, 241))
        self.lw_files_to.setObjectName("lw_files_to")
        self.btn_settings = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_settings.setGeometry(QtCore.QRect(10, 260, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.btn_settings.setFont(font)
        self.btn_settings.setObjectName("btn_settings")
        self.btn_receive = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_receive.setGeometry(QtCore.QRect(150, 260, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.btn_receive.setFont(font)
        self.btn_receive.setObjectName("btn_receive")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_send.setText(_translate("MainWindow", "send"))
        self.btn_settings.setText(_translate("MainWindow", "settings"))
        self.btn_receive.setText(_translate("MainWindow", "receive"))
