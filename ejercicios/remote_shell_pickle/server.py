import pickle
import socket
import subprocess 
import threading
import os

HEADER = 64
PORT = 5099
SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        pid_hilo = threading.get_ident()
        pid = os.getpid()
        msg = conn.recv(1024)

        descerializador = pickle.loads(msg)

        if descerializador != "exit":
            command = descerializador.split()
            returned = subprocess.run(command, capture_output=True)

            exit_code = bool(returned.returncode)
            if not exit_code:
                exit_stdout = str(returned.stdout,"utf-8")
                respuesta = bytes(f"OK\n {exit_stdout}", "utf-8")
            else:
                exit_stderr = str(returned.stderr,"utf-8")
                respuesta = bytes(f"ERROR\n{exit_stderr}", "utf-8")

            print(f"[{addr}] {descerializador}")
            conn.send(respuesta)
            
        if msg == DISCONNECT_MESSAGE:
                print(f"Proceso: {pid}, Hilo: {pid_hilo} ---> Disconnect")
                break
         
    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()