import socket
import sys

sock = socket.socket()
port = 8200
sock.bind(('127.0.0.1', port))

# сервер ожидает передачи информации
sock.listen(10)
    
while True:
	# начинаем принимать соединения
	conn, addr = sock.accept()

	# выводим информацию о подключении
	print('connected:', addr)
	k = (conn.recv(1024)).decode('UTF-8')

	if k is not "alDone":

		name_f = (conn.recv(1024)).decode('UTF-8')

		# открываем файл в режиме байтовой записи в отдельной папке 'sent'
		f = open(f"sent/{name_f}", "wb")

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

