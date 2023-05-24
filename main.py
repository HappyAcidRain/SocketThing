# база
import sys
from PyQt6 import QtWidgets, QtCore 
from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QTimer, QThread

# окно 
import MainUI

# подключение
import socket

# прочее
import pathlib

# основное окно
class MainWindow(QtWidgets.QMainWindow, MainUI.Ui_MainWindow, QDialog):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)

		self.setWindowTitle("SendThing")
		self.pb_progress.setValue(0)
		self.setFixedWidth(450)
		self.setFixedHeight(310)
		self.setAcceptDrops(True)

		self.an_list = QPropertyAnimation(self.lw_files_to, b"pos")
		self.an_label = QPropertyAnimation(self.lbl_pic, b"pos")

		self.btn_send.clicked.connect(self.sendFiles)

		self.filePlaylist = []

	def dragEnterEvent(self, event):
		mime = event.mimeData()

		if mime.hasUrls():
			event.acceptProposedAction()

	def dropEvent(self, event):

		for url in event.mimeData().urls():
			file_name = url.toLocalFile()
			self.lw_files_to.addItem(file_name)
			self.animation()
			self.updList()

		return super().dropEvent(event)

	def animation(self):

		self.an_list.setEasingCurve(QEasingCurve.Type.InOutCubic)
		self.an_list.setEndValue(QPoint(10, 10))
		self.an_list.setDuration(400)
		self.an_list.start()

		self.an_label.setEasingCurve(QEasingCurve.Type.InOutCubic)
		self.an_label.setEndValue(QPoint(-470, 10))
		self.an_label.setDuration(400)
		self.an_label.start()

	def updList(self):

		for x in range(self.lw_files_to.count()):
			item = self.lw_files_to.item(x)
			self.filePlaylist.append(str(item.text()))
			print(f"appended: {self.filePlaylist}")

	def sendFiles(self):

		ip = "localhost"
		port = 8200
		sock = socket.socket()
		sock.connect((ip,port))

		filesNum = 0

		while filesNum < len(self.filePlaylist):
			
			f_name = pathlib.PurePath(self.filePlaylist[filesNum]).name  
			sock.send((bytes(f_name, encoding = 'UTF-8')))

			# открываем файл в режиме байтового чтения
			f = open (self.filePlaylist[filesNum], "rb")

			# читаем строку
			l = f.read(1024)

			while (l):
				# отправляем строку на сервер
				sock.send(l)
				l = f.read(1024)

			f.close()

			filesNum += 1

		sock.close()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	m = MainWindow()
	m.show()	
	sys.exit(app.exec())
