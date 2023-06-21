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

		ip = ip.replace("(","")
		ip = ip.replace(")","")
		ip = ip.replace(",","")
		self.IP = ip.replace("'","")

		port = port.replace("(","")
		port = port.replace(")","")
		self.PORT = port.replace(",","")

		path = path.replace("(","")
		path = path.replace(")","")
		path = path.replace(",","")
		self.PATH = path.replace("'","")

		connect.close()

	def server(self):

		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind(self.ADDR)
		server.listen()

		print("1")

		self.send("[STARTING] Server has been started and now listening.")
		self.send("[INFO] Server's addr is: " + str(self.IP) + ":"+ str(self.PORT))
		self.send("[INFO] You can change ip and port by editing server.py file")

		print("23")
 
		while self.state:
			# разрешаем подключение 
			conn, addr = server.accept()
			self.send(f"[NEW CONNECTION] {addr} connected.")

			print("2")
        
			# получаем имя файла и расширение 
			filename = conn.recv(1024).decode("utf-8")
			self.send(f"[RECV] Receiving the filename.")
			file = open(f"{self.PATH}/{filename}", "wb")
			conn.send("Filename received.".encode("utf-8"))
 
			# получаем файл
			self.send(f"[RECV] Receiving the file data.")

			while self.state:
				data = conn.recv(1024)
				file.write(data)

				if not data:
					break

			conn.send("File data received".encode("utf-8"))
 
			# завершаем
			file.close()
			conn.close()
			self.send(f"[DISCONNECTED] {addr} disconnected.")

			if self.state == False:
				break

	def changeState(self):
		if self.state:
			self.state = False
		else:
			self.state = True

	def send(self, message):
		self.message.emit(message)

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

		connect = sqlite3.connect("settings.db")
		cursor = connect.cursor()

		cursor.execute("SELECT clientIp FROM savedData WHERE rowid = 1")
		ip = str(cursor.fetchone())

		cursor.execute("SELECT clientPort FROM savedData WHERE rowid = 1")
		port = str(cursor.fetchone())

		ip = ip.replace("(","")
		ip = ip.replace(")","")
		ip = ip.replace("'", "")
		self.ip = ip.replace(",","")

		port = port.replace("(","")
		port = port.replace(")","")
		self.port = port.replace(",","")

		print(self.ip + ":" + self.port)

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
		self.btn_close.clicked.connect(lambda: self.close())

		connect = sqlite3.connect("settings.db")
		cursor = connect.cursor()

		cursor.execute("SELECT clientIp FROM savedData WHERE rowid = 1")
		clientIp = str(cursor.fetchone())

		clientIp = clientIp.replace("(","")
		clientIp = clientIp.replace(")","")
		clientIp = clientIp.replace(",","")
		clientIp = clientIp.replace("'","")

		cursor.execute("SELECT clientPort FROM savedData WHERE rowid = 1")
		clientPort = str(cursor.fetchone())

		clientPort = clientPort.replace("(","")
		clientPort = clientPort.replace(")","")
		clientPort = clientPort.replace(",","")

		cursor.execute("SELECT serverIp FROM savedData WHERE rowid = 1")
		serverIp = str(cursor.fetchone())

		serverIp = serverIp.replace("(","")
		serverIp = serverIp.replace(")","")
		serverIp = serverIp.replace(",","")
		serverIp = serverIp.replace("'","")

		cursor.execute("SELECT serverPort FROM savedData WHERE rowid = 1")
		serverPort = str(cursor.fetchone())

		serverPort = serverPort.replace("(","")
		serverPort = serverPort.replace(")","")
		serverPort = serverPort.replace(",","")

		cursor.execute("SELECT serverPath FROM savedData WHERE rowid = 1")
		serverPath = str(cursor.fetchone())

		serverPath = serverPath.replace("(","")
		serverPath = serverPath.replace(")","")
		serverPath = serverPath.replace(",","")
		serverPath = serverPath.replace("'","")

		connect.close()

		self.le_clientIp.setPlaceholderText(clientIp)
		self.le_clientPort.setPlaceholderText(clientPort)
		self.le_serverIp.setPlaceholderText(serverIp)
		self.le_serverPort.setPlaceholderText(serverPort)
		self.le_path.setPlaceholderText(serverPath)

	def save(self):

		connect = sqlite3.connect("settings.db")
		cursor = connect.cursor()

		ip = self.le_clientIp.text()
		port = self.le_clientPort.text()

		cursor.execute(f"UPDATE savedData SET clientIp = '{ip}' WHERE rowid = 1 ")
		cursor.execute(f"UPDATE savedData SET clientPort = '{port}' WHERE rowid = 1 ")
		connect.commit()
		connect.close()

		self.le_clientIp.setPlaceholderText(ip)
		self.le_clientPort.setPlaceholderText(port)

# окно сервера 
class ServerWindow(QtWidgets.QMainWindow, serverUI.Ui_MainWindow, QDialog):
	def __init__(self):
		super(ServerWindow, self).__init__()
		self.setupUi(self)

		self.setWindowTitle("SendThing server")
		self.btn_close.clicked.connect(self.stopAndClose)
		self.btn_start.clicked.connect(self.start)

		self.serverThread = ServerThread()
		self.serverThread.message.connect(self.console)

	def console(self, message):
		self.te_console.append(message)

	def stopAndClose(self):
		self.serverThread.changeState()
		self.close()

	def start(self):
		self.serverThread.changeState()
		self.serverThread.server()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	m = MainWindow()
	m.show()	
	sys.exit(app.exec())
