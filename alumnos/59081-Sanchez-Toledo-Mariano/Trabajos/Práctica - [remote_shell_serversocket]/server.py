from socket import *
from subprocess import *
from threading import *
import pickle


class Client(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        try:
            conexion = self.conn
            while True:
                if conexion == '':
                    continue
                comando = conexion.recv(1024)
                comando = pickle.loads(comando)
                if comando == 'stop':
                    conexion.close()
                    exit(0)
                elif comando == None or comando == '':
                    continue
                print('Comando recibido:\n', comando)
                out = getoutput(comando)
                newout = pickle.dumps(out)
                conexion.send(newout)
        except:
            pass

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