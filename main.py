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

	def dragEnterEvent(self, event):
		# Тут выполняются проверки и дается (или нет) разрешение на Drop

		mime = event.mimeData()

		# Если перемещаются ссылки
		if mime.hasUrls():
			# Разрешаем
			event.acceptProposedAction()

	def dropEvent(self, event):
		# Обработка события Drop

		for url in event.mimeData().urls():
			file_name = url.toLocalFile()
			self.lw_files_to.addItem(file_name)
			self.animation()

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

	def sendFiles(self):

		items = []

		for x in range(self.lw_files_to.count()-1):
			items.append(str(self.lw_files_to.item(x)))

		ip = "31.131.73.30"
		port = 8200
		sock = socket.socket()
		sock.connect((ip,port))

		for item in items:

			f_name = pathlib.PurePath(items(item)).name  
			sock.send((bytes(f_name, encoding = 'UTF-8')))

			# открываем файл в режиме байтового чтения
			f = open (items(item), "rb")

			# читаем строку
			l = f.read(1024)

			while (l):
				# отправляем строку на сервер
				sock.send(l)
				l = f.read(1024)

		k = "alDone"
		sock.send(bytes(k, encoding = 'UTF-8'))

		f.close()
		sock.close()
	
if __name__ == '__main__':
	app = QApplication(sys.argv)
	m = MainWindow()
	m.show()	
	sys.exit(app.exec())
