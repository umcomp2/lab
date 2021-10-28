from parseServer import Parse
from socket import *
from threading import *
from os import O_CREAT
import pickle


class ClientTCP(Thread):
    def __init__(self, conn, addr, filename):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.fd = open(filename, 'w', O_CREAT)

    def run(self):
        conexion = self.conn
        fd = self.fd
        conexion.send(pickle.dumps('Esperando Input'))
        texto = conexion.recv(1024)
        texto = pickle.loads(texto)
        print('Texto recibido:\n', texto)
        fd.write(texto)
        fd.close()
        conexion.close()
        print('Conexion', self.addr, 'fue cerrada')
        exit(0)

class CLientUDP(Thread):
    def __init__(self, socket, filename):
        Thread.__init__(self)
        self.socket = socket
        self.fd = open(filename, 'w', O_CREAT)

    def run(self):
        socket = self.socket
        fd = self.fd
        texto, addr = socket.recvfrom(1024)
        texto = pickle.loads(texto)
        print('Texto recibido:\n', texto)
        fd.write(texto)
        fd.close()
        exit(0)





def tcp(miSocket):
    miSocket.bind(('localhost', args.port))
    miSocket.listen(1)
    conn, addr = miSocket.accept()
    client = ClientTCP(conn, addr, args.file)
    client.start()
    print("%s:%d se ha conectado." % addr)

def udp(miSocket):
    miSocket.bind(('localhost', args.port))
    client = CLientUDP(miSocket, args.file)
    client.start()



def main():
    global args
    args = Parse.parser()
    if args.type == 'udp':
        miSocket = socket(AF_INET, SOCK_DGRAM)
        udp(miSocket)
    elif args.type == 'tcp':
        miSocket = socket(AF_INET, SOCK_STREAM)
        tcp(miSocket)


if __name__ == '__main__':
    main()