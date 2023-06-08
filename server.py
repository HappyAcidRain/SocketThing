import socket
 
IP = "localhost"
PORT = 4455
ADDR = (IP, PORT)
 
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    print("[STARTING] Server has been started and now listening.")
    print("[INFO] Server's addr is: " + str(IP) + ":"+ str(PORT))
    print("[INFO] You can change ip and port by editing server.py file")
 
    while True:
        # разрешаем подключение 
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        
        # получаем имя файла и расширение 
        filename = conn.recv(1024).decode("utf-8")
        print(f"[RECV] Receiving the filename.")
        file = open(filename, "wb")
        conn.send("Filename received.".encode("utf-8"))
 
        # получаем файл
        print(f"[RECV] Receiving the file data.")

        while True:
            data = conn.recv(1024)
            file.write(data)

            if not data:
                break

        conn.send("File data received".encode("utf-8"))
 
        # завершаем
        file.close()
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")
 
if __name__ == "__main__":
    main()