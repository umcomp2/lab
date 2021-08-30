from socket import *
from subprocess import *
from threading import *

def waitConection():
    global conexion
    global addr
    conexion = ''
    while True:
        conexion, addr = miSocket.accept()
        print('Conexión establecida', addr)
        

def procesado():
    while True:
        if conexion == '':
            continue
        comando = conexion.recv(1024)
        if comando.decode() == 'stop':
            conexion.close()
        elif comando.decode() == None or comando.decode() == '':
            continue
        print('Comando recibido:\n', comando.decode())
        out = getoutput(comando.decode())
        conexion.send(out.encode())

if __name__ == '__main__':
    miSocket = socket()
    miSocket.bind(('localhost', 8001))
    miSocket.listen(1)

    th = Thread(target=waitConection).start()
    
    procesado()

    exit(0)