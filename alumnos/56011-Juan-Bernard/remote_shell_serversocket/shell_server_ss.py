import argparse
import pickle
import os
import signal
import socketserver
import subprocess as sp

# Función argparse para definir host y puerto
def argumentos():
    parser = argparse.ArgumentParser(description='Shell Server - Comandos')
    parser.add_argument('-ht', '--host', type=str, default='localhost',
                        help='Host de conexión para el server')
    parser.add_argument('-p', '--port', type=int, default=2222,
                        help='Puerto de conexión para el server')
    parser.add_argument('-m', '--mode', type=str, default='p',
                        help='Multicliente mediante forking o threading')
    return parser.parse_args()


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('Nueva conexión de dirección %s y puerto %d.' % (str(self.client_address[0]), self.client_address[1]))
        while True:
            self.comando_0 = self.request.recv(256)
            if not self.comando_0:
                break
            self.comando_1 = pickle.loads(self.comando_0)
            self.comando_2 = sp.Popen(self.comando_1, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            self.stdout, self.stderr = self.comando_2.communicate()
            if self.stdout:
                self.resultado = (b'OK\tPID: %d\n%s' % (os.getpid(), self.stdout))
            elif self.stderr:
                self.resultado = (b'ERROR\tPID: %d\n%s' % (os.getpid(), self.stderr))
            self.request.sendall(pickle.dumps(self.resultado))
        print('Conexión con dirección %s y puerto %d finalizada.' % (str(self.client_address[0]), self.client_address[1]))


class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    # Definir host y puerto
    args = argumentos()
    host = args.host
    port = args.port
    if args.mode == 'p':
        # Evitar procesos zombies
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        print('Esperando conexiones...')
        with ForkedTCPServer((host, port), MyTCPHandler) as server:
            server.serve_forever()
    elif args.mode == 't':
        print('Esperando conexiones...')
        with ThreadedTCPServer((host, port), MyTCPHandler) as server:
            server.serve_forever()
