import socket
import sys

ip = "31.131.73.30"
port = 8200

# создаём сокет для подключения
sock = socket.socket()
sock.connect((ip,port))

print("Connected!")

# запрашиваем имя файла и отправляем серверу
f_name = input ('File to recive: ')
sock.send((bytes(f_name, encoding = 'UTF-8')))

f = open(f_name, "wb")

while True:

		# получаем байтовые строки
		l = sock.recv(1024)

		# пишем байтовые строки в файл
		f.write(l)

		if not l:
			break

f.close()
sock.close()