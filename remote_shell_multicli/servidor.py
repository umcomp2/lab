import socket
import threading
import subprocess
# import os

HEADER = 64
PORT = 2030
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "\n---DESCONECTADO---"


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(ADDR)
serversocket.listen(5)
#conn=connection - addr=address

def handle_client(conn, addr):
    print(f"---NUEVA CONEXIÓN---\n {addr} conectado con exito.")
    
    while True:
        # pid_hilo = threading.get_ident()
        # pid = os.getpid()
        tamaño_msg = conn.recv(HEADER).decode(FORMAT)        
        if tamaño_msg:
            tamaño_msg = int(tamaño_msg)
            
            msg = conn.recv(tamaño_msg).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                # print(f"\nProceso: {pid}, Hilo: {pid_hilo} \n---> DESCONECTADO")
                break
            command = msg.split()
            print(command)
            returned = subprocess.run(command)

            exit_code = bool(returned.returncode)
            if not exit_code:
                exit_stdout = str(returned.stdout, 'utf-8')
                respuesta = bytes(f"OK\n {exit_stdout}", 'utf-8')
            else:
                exit_stderr = str(returned.stderr, 'utf-8')
                respuesta = bytes(f"ERROR\n{exit_stderr}", 'utf-8')

            print(f"[{addr}] {msg}")
            conn.send(respuesta)
    conn.close()

def start():
    serversocket.listen()
    while True:
        conn, addr = serversocket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"---CONEXIONES ACTIVAS--- {threading.activeCount() - 1}")

print("---STARTING--- El servidor ha comenzado...")
start()

