import socket
import threading
import datetime

MAX_SIZE = 512
KEY = "12135"
TODAY = datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

def thread_server(sock_sv):
    name = "_"
    key = "_"
    email = "_"
    sock,addr = sock_sv
    print("Launching thread - addr: %s" % str(addr))
    exit = False
    ip = str(addr)
    stage = 0
    while True:
        msg = sock.recv(MAX_SIZE).decode()
        if msg[0:5] =="hello": 
            if stage == 0:
                name = msg[6:]
                resp = "200"
                stage += 1
            else:
                resp = "400"
        elif msg[0:5] == "email":
            email = msg[6:]
            if stage == 1:
                email = msg[6:]
                resp = "200"
                stage += 1
            else:
                resp = "400"
        elif msg[0:3] == "key":
            if stage == 2:
                key = msg[4:-1]
                if key[:-1] != KEY:
                    resp ="404"
                else:
                    resp = "200"
                    stage += 1
            else:
                resp = "400"
        elif msg[0:4] == "exit":
            resp = "200"
            exit = True
        else:
            resp = "500"

        sock.send(resp.encode("ASCII"))
        if exit:
            data = "%s|%s|%s|%s|%s" % (TODAY,name,email,key,ip)
            data = data.replace('\n', '').replace('\r', '')
            print(data)
            sock.close()
            break
            
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ""
port= 2222

sock_server.bind((host, port))
sock_server.listen(5)

while True:
    client_socket = sock_server.accept()
    print("Connection from: %s" % str(client_socket[1]))
    th = threading.Thread(target=thread_server, args=(client_socket,))
    th.start()