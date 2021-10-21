import logging
from os import close
from parseServer import Parser
from subprocess import getoutput
import pickle
import sys
import socketserver
import socket
import threading


logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s',)

class RemoteRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('EchoRequestHandler')
        self.logger.debug('__init__')
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return


    def handle(self):
        self.logger.debug('handle')
        
        comando = self.request.recv(1024)
        comando = pickle.loads(comando)
        self.logger.debug('recv()->"%s"', comando)
        self.request.send(comando)
        out = pickle.dumps(getoutput(comando))
        self.request.send(out)
        return


class RemoteServer(socketserver.TCPServer):
    def __init__(self, server_address, handler_class=RemoteRequestHandler,):
        self.logger = logging.getLogger('EchoServer')
        self.logger.debug('__init__')
        socketserver.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        self.logger.debug('server_activate')
        socketserver.TCPServer.server_activate(self)
        return

    def serve_forever(self, poll_interval=0.5):
        self.logger.debug('waiting for request')
        socketserver.TCPServer.serve_forever(self, poll_interval)
        return
    
    def handle_request(self):
        self.logger.debug('hanlde_request')
        return socketserver.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)',
                          request, client_address)
        return socketserver.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s, %s)',
                          request, client_address)
        return socketserver.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        self.logger.debug('server_close')
        return socketserver.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)',
                          request, client_address)
        return socketserver.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        self.logger.debug('close_request(%s)', request_address)
        return socketserver.TCPServer.close_request(self, request_address)

    def shutdown(self):
        self.logger.debug('shutdown()')
        return socketserver.TCPServer.shutdown(self)


def main():
    args = Parser().parser()
    address = ('localhost', 8000)
    server = RemoteServer(address, RemoteRequestHandler)
    ip, port = server.server_address
    if args.m:
        #iniciateWithFork()
        pass
    
