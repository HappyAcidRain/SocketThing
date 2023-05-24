import socket
import sys

# создаём сокет и связываем его с IP-адресом и портом

sock = socket.socket()
port = 8200
sock.bind(('localhost', port))

print("server has been started!")

# сервер ожидает передачи информации
sock.listen(10)

while True:
	# начинаем принимать соединения
	conn, addr = sock.accept()

	# выводим информацию о подключении
	print('connected:', addr)

	# получаем название файла
	f_name = (conn.recv(1024)).decode('UTF-8')

	# открываем файл в режиме байтового чтения
	f = open(f"files/{f_name}", "rb")

	# читаем строку
	l = f.read(1024)

	while l:
		# отправляем строку клиенту
		conn.send(l)
		l=f.read(1024)

	f.close()
	conn.close()

	print('File sent!')

sock.close()