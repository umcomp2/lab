from operator import add
import socket
import pickle
from parse import parseServer
from threading import Thread
from worker import *

def operaciones(conn, addr):
    tarea = pickle.loads(conn.recv(1024))
    if tarea[0].lower() == 'suma':
        resultado = suma.delay(tarea[1], tarea[2])
        conn.send(pickle.dumps(str(resultado.get())))
    elif tarea[0].lower() == 'resta':
        resultado = resta.delay(tarea[1], tarea[2])
        conn.send(pickle.dumps(str(resultado.get())))
    elif tarea[0].lower() == 'multiplicar':
        resultado = multiplicar.delay(tarea[1], tarea[2])
        conn.send(pickle.dumps(str(resultado.get())))
    elif tarea[0].lower() == 'dividir':
        resultado = dividir.delay(tarea[1], tarea[2])
        conn.send(pickle.dumps(str(resultado.get())))
    else:
        conn.send('Error')
    print('Operation completed, the client {} has been disconected'.format(add))

def main(ip, port, queue):
    sock_server = socket.socket()
    sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_server.bind(((ip), int(port)))
    print('Server started at {}:{}'.format(ip, port))
    sock_server.listen(queue)
    while True:
        conn, addr = sock_server.accept()
        print('connection established with the client {}'.format(addr))
        thr = Thread(target=operaciones, args=(conn, addr))
        thr.start()

if __name__ == '__main__':
    args = parseServer()
    IP, PORT = args.ip, args.port
    main(IP, PORT, 5)