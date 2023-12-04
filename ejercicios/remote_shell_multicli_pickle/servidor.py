import socket
import threading
import subprocess
import pickle


PORT = 2064
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = b"\n---DESCONECTADO---"


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(ADDR)
serversocket.listen(5)
#conn=connection - addr=address

def handle_client(conn, addr):
    print(f"---NUEVA CONEXIÓN---\n {addr} conectado con exito.")
    
    while True:
        msg = conn.recv(4096)       
        deserializado = pickle.loads(msg)
        if deserializado == DISCONNECT_MESSAGE:    
            break
        else:
            command = deserializado.split()
            process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            salida = pickle.dumps(stdout)
            error = pickle.dumps(stderr)
            conn.send(salida)
            conn.send(error)
        
        print(f"[{addr}] {deserializado}")
        conn.send(deserializado)
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

