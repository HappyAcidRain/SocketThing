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

		self.btn_send.clicked.connect(self.sendFiles)

		self.filePlaylist = []
		self.ip = 0
		self.port = 0

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

	def sendMagic(self, file):

		addr = (self.ip, self.port)
		FORMAT = "utf-32-le"

		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(addr)

		""" Opening and reading the file data. """
		f_name = pathlib.PurePath(file).name
		openedFile = open(file, "rb")
		data = openedFile.read(1024)

		""" Sending the filename to the server. """
		client.send(f_name.encode(FORMAT))
		msg = client.recv(1024).decode(FORMAT)
		print(f"[SERVER]: {msg}")

		""" Sending the file data to the server. """
		while (data):
			client.send(data)
			data = openedFile.read(1024)

		""" Closing the file. """
		openedFile.close()

		""" Closing the connection from the server. """
		client.close()

	def sendFiles(self):

		self.ip = self.le_ip.text()
		self.port = int(self.le_port.text())

		filesNum = 0

		while filesNum <= len(self.filePlaylist)-1 :
			self.sendMagic(self.filePlaylist[filesNum])
			filesNum += 1


if __name__ == '__main__':
	app = QApplication(sys.argv)
	m = MainWindow()
	m.show()	
	sys.exit(app.exec())
