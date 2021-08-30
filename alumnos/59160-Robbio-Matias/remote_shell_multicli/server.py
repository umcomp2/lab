import socket
import threading
import sys
import subprocess

PORT = int(sys.argv[1])
SERVER= "127.0.0.1"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((SERVER,PORT))

def client_handler(conn, addr):
        print(f"Nueva conexion establecida[cliente:{addr}]")
        connected  = True
        while connected:
            msg = conn.recv(4096).decode('utf-8')
            if msg == '!DISCONNECT':
                conn.close()
                print(f"Conexion finalizada[cliente:{addr}]")
                break

            cmd = msg.split()
            estado_cmd = subprocess.run(cmd,capture_output=True)
            if estado_cmd.returncode == 0:
                correct_output = estado_cmd.stdout.decode("utf-8")
                msg_back = bytes(f"OK\n{correct_output}", "utf-8")
                conn.send(msg_back)
            else:
                error_output = estado_cmd.stderr.decode("utf-8")
                msg_back = bytes(f"ERROR\n{error_output}", "utf-8")
                conn.send(msg_back)
            


#Esta funcion inizializa el server para comenzar a escuchar conexiones
def start_server():
    server.listen()
    print(F"Servidor inizializado y escuchando en {SERVER}")
    while True:
        conn, addr = server.accept()
        #En esta parte se inicializa un hilo por cada conexion que acepta para asi manejar varias conexiones al mismo tiempo
        #para esto crea un hilo por cada conexion utilizando la funcion client_handler que se encarga de manejar las solicitudes de cada cliente
        thread = threading.Thread(target=client_handler,args=(conn,addr))
        thread.start()


print("Inizializando Servidor....")
start_server()
