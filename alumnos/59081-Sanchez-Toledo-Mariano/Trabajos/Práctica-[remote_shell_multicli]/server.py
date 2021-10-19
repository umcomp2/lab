from socket import *
from subprocess import *
from threading import *


class Client(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        conexion = self.conn
        while True:
            if conexion == '':
                continue
            comando = conexion.recv(1024)
            if comando.decode() == 'stop':
                conexion.close()
                del self
            elif comando.decode() == None or comando.decode() == '':
                continue
            print('Comando recibido:\n', comando.decode())
            out = getoutput(comando.decode())
            conexion.send(out.encode())

def main():
    miSocket = socket()
    miSocket.bind(('localhost', 8001))
    miSocket.listen(3)
    while True:
        conn, addr = miSocket.accept()
        client = Client(conn, addr)
        client.start()
        print("%s:%d se ha conectado." % addr)

if __name__ == '__main__':
    main()