import socket
import sys

sock = socket.socket()
port = 8200
sock.bind(('localhost', port))

# сервер ожидает передачи информации
sock.listen(10)
    
while True:
	# начинаем принимать соединения
	conn, addr = sock.accept()

	# выводим информацию о подключении
	print('connected:', addr)
	k = (conn.recv(1024)).decode('UTF-16')
	print(k)

	if k != "alDone":

		# открываем файл в режиме байтовой записи в отдельной папке 'sent'
		f = open("recived/" + k, "wb")

		while True:

			# получаем байтовые строки
			l = conn.recv(1024)

			# пишем байтовые строки в файл на сервере
			f.write(l)

			if not l:
				break

		f.close()

	else:
		conn.close()

sock.close()

