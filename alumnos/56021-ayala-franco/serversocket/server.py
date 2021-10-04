import socket
import socketserver
import subprocess
import pickle
import signal
import argparse

def salir(uno, dos):
    server.shutdown()
    exit(0)

signal.signal(signal.SIGINT, salir)

def get_server(type: str):
    addr = ("127.0.0.1", 57001)
    if type == "p":
        return socketserver.ForkingTCPServer(addr, MyRequestHandler)
    if type == "t":
        return socketserver.ThreadingTCPServer(addr, MyRequestHandler)
    return None

class MyRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(100.0)
        while True:
            try:
                command = self.request.recv(100)
                result = subprocess.run(command, capture_output=True, encoding="UTF-8")
            except socket.timeout:
                break
            response = pickle.dumps(result)
            self.request.send(response)
        self.request.shutdown(socket.SHUT_RDWR)

parser = argparse.ArgumentParser()
parser.add_argument("-m", type=str, default="t", choices=["p", "t"])
args = parser.parse_args()

with get_server(args.m) as server:
    server.serve_forever()
