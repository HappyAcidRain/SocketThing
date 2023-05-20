import socket
import sys

ip = "31.131.73.30"
port = 8200

# создаём сокет для подключения
sock = socket.socket()
sock.connect((ip,port))

# запрашиваем имя файла и отправляем серверу
f_name = input ('File to send: ')
sock.send((bytes(f_name, encoding = 'UTF-8')))

# открываем файл в режиме байтового чтения
f = open (f_name, "rb")

# читаем строку
l = f.read(1024)

while l:
    # отправляем строку на сервер
    sock.send(l)
    l=f.read(1024)

f.close()
sock.close()