from socket import *
from parseCli import Parser
import os
import time
import pickle

def log(data, respuesta, hora, fecha):
    if args.log:
        with open('log.txt', 'a+', os.O_CREAT) as fd:
            fd.write('\n' + fecha + ' ' + hora)
            fd.write('\nComando:\n')
            fd.write(data)
            fd.write('\nRespuesta:\n')
            fd.write(respuesta+'\n')
            fd.close()

def processing(socket):
    global data
    global respuesta
    while True:
        hora = time.strftime("%H:%M:%S")
        fecha = time.strftime("%d/%m/%y")
        comando = input('Ingrese comando:\n')
        if comando == 'stop':
            break
        newComando = pickle.dumps(comando)
        socket.send(newComando)
        respuesta = socket.recv(1024)
        respuesta = pickle.loads(respuesta)
        print('Respuesta:\n',respuesta)
        if args.log:
            log(comando, respuesta, hora, fecha)


if __name__ == '__main__':
    miSocket = socket()
    miSocket.connect(('localhost', 8000))
    args = Parser.parser()
    processing(miSocket)
    miSocket.close()
    exit(0)