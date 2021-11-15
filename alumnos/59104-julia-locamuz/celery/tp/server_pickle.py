
import socket
import os
from calculadora import *
from _thread import *
import pickle

def threaded_client(connection):
    parametros = pickle.loads(connection.recv(1024))
    print(parametros)
    if parametros[0] == '+':
        print('here')
        operacion = suma.delay(parametros[1], parametros[2])
        resultado = operacion.get(timeout=5)

    elif parametros[0] == '-':
        operacion = resta.delay(parametros[1], parametros[2])
        resultado = operacion.get()

    elif parametros[0] == '*':
        operacion = mult.delay(parametros[1], parametros[2])
        resultado = operacion.get()

    elif parametros[0] == '/':
        operacion = div.delay(parametros[1], parametros[2])
        resultado = operacion.get()

    elif parametros[0] == '**':
        operacion = pot.delay(parametros[1], parametros[2])
        resultado = operacion.get()
    connection.send(pickle.dumps(resultado))
    connection.close()


if __name__ == '__main__':
    ServerSocket = socket.socket()
    host = '127.0.0.1'
    port = 1233
    ThreadCount = 0
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print('Waitiing for a connection..')
    ServerSocket.listen(5)

    while True:
        Client, address = ServerSocket.accept()
        print('conected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
        # CELERYYYYYYYY
    ServerSocket.close()
