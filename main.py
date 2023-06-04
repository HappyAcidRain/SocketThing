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

# таймер
class TimerThread(QtCore.QThread):
	s_timer = QtCore.pyqtSignal(int)

	def  __init__(self):
		QtCore.QThread.__init__(self)

		self.state = 1

	def run(self):
		self.sleep(1)
		self.s_timer.emit(self.state)
		

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
		self.lw_files_to.itemClicked.connect(self.cleaning)

		self.thread = TimerThread()
		self.thread.s_timer.connect(self.changeFormat)

		self.filePlaylist = []
		self.tempPlaylist = []
		self.ip = 0
		self.port = 0

	def dragEnterEvent(self, event):
		mime = event.mimeData()

		if mime.hasUrls():
			event.acceptProposedAction()

	def dropEvent(self, event):

		for url in event.mimeData().urls():
			file_name = url.toLocalFile()
			if file_name not in self.filePlaylist:
				self.lw_files_to.addItem(file_name)
				self.status("Status: file added")
			else:
				self.status("Status: Error: that/these file already in!")

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
			self.tempPlaylist.append(item.text())

		# удаляем повторяющиеся пути 
		self.filePlaylist = list(set(self.tempPlaylist))

	def sendMagic(self, file):

		addr = (self.ip, self.port)
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(addr)

		# открываем файл
		f_name = pathlib.PurePath(file).name
		openedFile = open(file, "rb")
		data = openedFile.read(1024)

		# отправляем имя файла и расширение 
		client.send(f_name.encode("utf-8"))
		msg = client.recv(1024).decode("utf-8")
		print(f"[SERVER]: {msg}")

		# отправляем файл
		while (data):
			client.send(data)
			data = openedFile.read(1024)

		# завершаем 
		openedFile.close()
		client.close()

	def sendFiles(self):

		self.pb_progress.setRange(0, self.lw_files_to.count())

		self.ip = self.le_ip.text()
		self.port = int(self.le_port.text())

		filesNum = 0

		while filesNum <= len(self.filePlaylist)-1 :
			self.sendMagic(self.filePlaylist[filesNum])
			filesNum += 1
			self.pb_progress.setValue(filesNum)

			if self.pb_progress.value() == self.lw_files_to.count():
				self.status("Status: all files has been sent!")
				self.pb_progress.setValue(0)

	def cleaning(self):
		try:
			item = self.lw_files_to.currentItem()
			self.lw_files_to.takeItem(self.lw_files_to.row(item))
			self.filePlaylist.remove(str(item.text()))
			self.status("Status: file unselected")
			
		except ValueError:
			self.filePlaylist.clear()

	def changeFormat(self, state):
		if state == 1:
			self.pb_progress.setFormat('%p%')

	def status(self, text):
		self.pb_progress.setFormat(text)
		self.thread.start()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	m = MainWindow()
	m.show()	
	sys.exit(app.exec())
