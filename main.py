# база
import sys
from PyQt6 import QtWidgets, QtCore 
from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QTimer, QThread

# окно 
import MainUI

# подключение
import os
import socket
import struct

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

		self.btn_send.clicked.connect(self.sendMultipleFiles)

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
			self.filePlaylist.append(item.text())
		print(f"appended: {self.filePlaylist}")

	def sendFiles(self, file):

		@staticmethod
		def send_file(sck: socket.socket, filename):

			# Получение размера файла.
			filesize = os.path.getsize(filename)

			# В первую очередь сообщим серверу, 
			# сколько байт будет отправлено.

			sck.sendall(struct.pack("<Q", filesize))

			# Отправка файла блоками по 1024 байта.
			with open(filename, "rb") as f:
				while read_bytes := f.read(1024):
					sck.sendall(read_bytes)

		with socket.create_connection(("localhost", 6190)) as conn:

			# отправим имя файла
			f_name = pathlib.PurePath(file).name  
			conn.send((bytes(f_name, encoding = 'UTF-16')))

			print("Подключение к серверу.")
			print("Передача файла...")
			send_file(conn, file)
			print("Отправлено.")

		print("Соединение закрыто.")

	def sendMultipleFiles(self):

		filesNum = 0

		while filesNum <= len(self.filePlaylist)-1 :
			self.sendFiles(self.filePlaylist[filesNum])
			filesNum += 1


if __name__ == '__main__':
	app = QApplication(sys.argv)
	m = MainWindow()
	m.show()	
	sys.exit(app.exec())
