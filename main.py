# база
import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QTimer, QThread

# окна
import MainUI
import settingsUI
import serverUI

# подключение
import os
import socket
import struct

# прочее
import pathlib
import sqlite3

# сокращение вывода БД
def textTrans(text, QuoteMode):
	if QuoteMode:
		text = text.replace("(","")
		text = text.replace(")","")
		text = text.replace(",","")
		text = text.replace("'","")
		return text

	else:
		text = text.replace("(","")
		text = text.replace(")","")
		text = text.replace(",","")
		return text


# таймер
class TimerThread(QtCore.QThread):
	s_timer = QtCore.pyqtSignal(int)

	def  __init__(self):
		QtCore.QThread.__init__(self)

		self.state = 1

	def run(self):
		self.sleep(1)
		self.s_timer.emit(self.state)

# сервер 
class ServerThread(QtCore.QThread):
	message = QtCore.pyqtSignal(str)

	def  __init__(self):
		QtCore.QThread.__init__(self)

		self.state = False

		self.IP = None
		self.PORT = None
		self.PATH = None

		self.readSettings()
		self.ADDR = (self.IP, int(self.PORT))

	def readSettings(self):

		connect = sqlite3.connect("settings.db")
		cursor = connect.cursor()

		cursor.execute("SELECT serverIp FROM savedData WHERE rowid = 1")
		ip = str(cursor.fetchone())

		cursor.execute("SELECT serverPort FROM savedData WHERE rowid = 1")
		port = str(cursor.fetchone())

		cursor.execute("SELECT serverPath FROM savedData WHERE rowid = 1")
		path = str(cursor.fetchone())

		self.IP = textTrans(ip, True)
		self.PORT = textTrans(port, False)
		self.PATH = textTrans(path, True)

		connect.close()

	def run(self):

		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind(self.ADDR)
		server.listen()

		self.message.emit("[STARTING] Server has been started and now listening.")
		self.message.emit("[INFO] Server's addr is: " + str(self.IP) + ":"+ str(self.PORT))
 
		while self.state:
			# разрешаем подключение 
			conn, addr = server.accept()
			self.message.emit(f"[CONNECTION] {addr} connected.")
        
			# получаем имя файла и расширение 
			filename = conn.recv(1024).decode("utf-8")
			self.message.emit(f"[RECV] Receiving the filename.")
			file = open(f"{self.PATH}/{filename}", "wb")
 
			# получаем файл
			self.message.emit(f"[RECV] Receiving the file data.")

			while self.state:
				data = conn.recv(1024)
				file.write(data)

				if not data:
					break

			self.message.emit(f"[DONE] The file is received successfuly.")
 
			# завершаем
			file.close()
			conn.close()
			self.message.emit(f"[CONNECTION] {addr} disconnected.")

			if self.state == False:
				break

	def changeState(self):
		if self.state:
			self.state = False
		else:
			self.state = True

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

		app_icon = QtGui.QIcon()
		app_icon.addFile('assets/icon90.png', QtCore.QSize(90,90))
		self.setWindowIcon(app_icon)

		self.an_list = QPropertyAnimation(self.lw_files_to, b"pos")
		self.an_label = QPropertyAnimation(self.lbl_pic, b"pos")

		self.btn_send.clicked.connect(self.sendFiles)
		self.btn_receive.clicked.connect(self.serverWin)
		self.btn_settings.clicked.connect(self.settingsWin)
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

		ADDR = (self.ip, int(self.port))
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(ADDR)

		# открываем файл
		f_name = pathlib.PurePath(file).name
		openedFile = open(file, "rb")
		data = openedFile.read(1024)

		# отправляем имя файла и расширение 
		client.send(f_name.encode("utf-8"))

		# отправляем файл
		while (data):
			client.send(data)
			data = openedFile.read(1024)

		# завершаем 
		openedFile.close()
		client.close()

	def sendFiles(self):

		if len(self.filePlaylist) != 0:

			connect = sqlite3.connect("settings.db")
			cursor = connect.cursor()

			cursor.execute("SELECT clientIp FROM savedData WHERE rowid = 1")
			ip = str(cursor.fetchone())

			cursor.execute("SELECT clientPort FROM savedData WHERE rowid = 1")
			port = str(cursor.fetchone())
 
			self.ip = textTrans(ip, True)
			self.port = textTrans(port, True)

			connect.close()

			self.pb_progress.setRange(0, self.lw_files_to.count())

			filesNum = 0

			while filesNum <= len(self.filePlaylist)-1 :
				self.sendMagic(self.filePlaylist[filesNum])
				filesNum += 1
				self.pb_progress.setValue(filesNum)

				if self.pb_progress.value() == self.lw_files_to.count():
					self.status("Status: all files has been sent!")
					self.pb_progress.setValue(0)

		else:
			self.status("No files has been added!")

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

	def settingsWin(self):
		self.settings = SettingWindow()
		self.settings.show()

	def serverWin(self):
		self.server = ServerWindow()
		self.server.show()

# окно настроек
class SettingWindow(QtWidgets.QMainWindow, settingsUI.Ui_MainWindow, QDialog):
	def __init__(self):
		super(SettingWindow, self).__init__()
		self.setupUi(self)

		self.setWindowTitle("SendThing settings")
		self.setFixedWidth(340)
		self.setFixedHeight(350)

		app_icon = QtGui.QIcon()
		app_icon.addFile('assets/icon90.png', QtCore.QSize(90,90))
		self.setWindowIcon(app_icon)

		self.btn_save.clicked.connect(self.save)
		self.btn_close.clicked.connect(self.close)

		connect = sqlite3.connect("settings.db")
		cursor = connect.cursor()

		cursor.execute("SELECT clientIp FROM savedData WHERE rowid = 1")
		clientIp = str(cursor.fetchone())
		clientIp = textTrans(clientIp, True)

		cursor.execute("SELECT clientPort FROM savedData WHERE rowid = 1")
		clientPort = str(cursor.fetchone())
		clientPort = textTrans(clientPort, False)

		cursor.execute("SELECT serverIp FROM savedData WHERE rowid = 1")
		serverIp = str(cursor.fetchone())
		serverIp = textTrans(serverIp, True)

		cursor.execute("SELECT serverPort FROM savedData WHERE rowid = 1")
		serverPort = str(cursor.fetchone())
		serverPort = textTrans(serverPort, False)

		cursor.execute("SELECT serverPath FROM savedData WHERE rowid = 1")
		serverPath = str(cursor.fetchone())
		serverPath = textTrans(serverPath, True)

		connect.close()

		self.le_clientIp.setPlaceholderText(clientIp)
		self.le_clientPort.setPlaceholderText(clientPort)
		self.le_serverIp.setPlaceholderText(serverIp)
		self.le_serverPort.setPlaceholderText(serverPort)
		self.le_path.setPlaceholderText(serverPath)

	def save(self):

		connect = sqlite3.connect("settings.db")
		cursor = connect.cursor()

		clientIp = ''
		clientPort = ''
		serverIp = ''
		serverPort = ''
		serverPath = ''

		enum = [
			[serverIp, 'serverIp', self.le_serverIp],
			[serverPort, 'serverPort', self.le_serverPort],
			[serverPath, 'serverPath', self.le_path],
			[clientIp, 'clientIp', self.le_clientIp],
			[clientPort, 'clientPort', self.le_clientPort]
			]

		for first, second, third in enum:
			if third.text() != '':
				first = third.text()
				third.setPlaceholderText(first)
				cursor.execute(f"UPDATE savedData SET {second} = '{first}' WHERE rowid = 1 ")
				connect.commit()
		
		connect.close()

# окно сервера 
class ServerWindow(QtWidgets.QMainWindow, serverUI.Ui_MainWindow, QDialog):
	def __init__(self):
		super(ServerWindow, self).__init__()
		self.setupUi(self)

		self.signal = False

		self.setWindowTitle("SendThing server")
		self.lbl_savePath.setStyleSheet("color: rgb(130, 130, 130); font: 10px ComicSans MS")
		self.btn_close.clicked.connect(self.close)
		self.viewPath()

		self.serverThread = ServerThread()
		self.serverThread.message.connect(self.console)

		self.serverThread.changeState()
		self.serverThread.start()

	def viewPath(self):
		connect = sqlite3.connect("settings.db")
		cursor = connect.cursor()

		cursor.execute("SELECT serverPath FROM savedData WHERE rowid = 1")
		serverPath = str(cursor.fetchone())
		serverPath = textTrans(serverPath, True)

		self.lbl_savePath.setText(" Files will be saved here: " + serverPath)

		connect.close()

	def console(self, message):
		self.te_console.append(message)

	def closeEvent(self, event):

		self.serverThread.changeState()
			

if __name__ == '__main__':
	app = QApplication(sys.argv)
	m = MainWindow()
	m.show()	
	sys.exit(app.exec())
