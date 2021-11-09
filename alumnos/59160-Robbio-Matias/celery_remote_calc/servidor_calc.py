import socket
import argparse
from tasks import *
import threading


def client_handler(conn, addr):
        print(f"Nueva conexion establecida[cliente:{addr}]")
        connected  = True
        while connected:
            msg = conn.recv(4096).decode('utf-8')
            msg = msg.split()
            n = msg[1]
            m = msg[2]
            if msg[0] == 'suma':
                send_to_cola = suma.delay(n,m)
            elif msg[0] == 'resta':
                send_to_cola = resta.delay(n,m)
            elif msg[0] == 'mult':
                send_to_cola = mult.delay(n,m)
            elif msg[0] == 'div':
                send_to_cola = div.delay(n,m)
            elif msg[0] == 'pot':
                send_to_cola = pot.delay(n,m)

            resultado = str(send_to_cola.get())
            conn.send(bytes(resultado,"utf-8"))
            conn.close
                      
def start_server():
    server.listen()
    print(F"Servidor inizializado y escuchando en {SERVER}")
    while True:
        conn, addr = server.accept()
        #En esta parte se inicializa un hilo por cada conexion que acepta para asi manejar varias conexiones al mismo tiempo
        #para esto crea un hilo por cada conexion utilizando la funcion client_handler que se encarga de manejar las solicitudes de cada cliente
        thread = threading.Thread(target=client_handler,args=(conn,addr))
        thread.start()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server',action="store",default='0.0.0.0', type= str)
    parser.add_argument('-p', '--port',action="store", type= int, required=True)
    args = parser.parse_args()

    SERVER = args.server
    PORT = args.port

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((SERVER,PORT))

    print("Inizializando Servidor....")
    start_server()
