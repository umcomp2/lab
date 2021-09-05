from socket import *
from parseCli import Parser


def processing(socket):
    while True:
        comando = input('Ingrese comando:\n')
        socket.send(comando.encode())
        respuesta = socket.recv(1024).decode()
        if comando == 'exit':
            socket.close()
            exit(0)
        print('Respuesta:\n',respuesta)


if __name__ == '__main__':
    args = Parser.parser()
    miSocket = socket()
    miSocket.connect((args.ip, args.port))
    processing(miSocket)
    exit(0)
