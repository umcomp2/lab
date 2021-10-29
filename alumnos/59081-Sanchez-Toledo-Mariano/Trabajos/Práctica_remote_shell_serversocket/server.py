import logging
from os import close, name, waitpid
from parseServer import Parser
from subprocess import getoutput
import pickle
import sys
import socketserver
import socket
import threading


logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s',)

class RemoteRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            comando = self.request.recv(1024)
            comando = pickle.loads(comando)
            print('recv()->"%s"', comando)
            out = pickle.dumps(getoutput(comando))
            self.request.send(out)
        



def main():
    args = Parser.parser()
    host, port = 'localhost', 8000

    if args.mode == 't':
        with socketserver.ThreadingTCPServer((host, port), RemoteRequestHandler) as server:
            print('Serving at {}:{}'.format(host, port))
            server.serve_forever()
    elif args.mode == 'p':
        with socketserver.ForkingTCPServer((host, port), RemoteRequestHandler) as server:
            print('Serving at {}:{}'.format(host, port))
            server.serve_forever()

if __name__ == '__main__':
    main()