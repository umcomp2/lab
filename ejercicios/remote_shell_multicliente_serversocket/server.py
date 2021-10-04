import socketserver
import threading
import pickle
import subprocess
import argparse

DISCONNECT_MESSAGE = "!DISCONNECT"

parser = argparse.ArgumentParser(description= "Socket TCP")
parser.add_argument("-m", "--type", dest = "tipo", required = True, help ="Forking/Threading")

args = parser.parse_args()
type = args.tipo

class MyTCPHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        connected = True
        while connected:
            msg = self.data = self.request.recv(1024).strip()
            descerializador = pickle.loads(msg)
            if descerializador != DISCONNECT_MESSAGE:
                command = descerializador.split()
                returned = subprocess.run(command, capture_output=True)

                exit_code = bool(returned.returncode)
                if not exit_code:
                    exit_stdout = str(returned.stdout,"utf-8")
                    respuesta = bytes(f"OK\n {exit_stdout}", "utf-8")
                    self.request.send(respuesta)
                else:
                    exit_stderr = str(returned.stderr,"utf-8")
                    respuesta = bytes(f"ERROR\n{exit_stderr}", "utf-8")
                    self.request.send(respuesta)

            if descerializador == DISCONNECT_MESSAGE:
                print("[DISCONNECT]")
                break
                    
class ThreadTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedTCPServer(socketserver.ForkingMixIn,socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9998
    socketserver.TCPServer.allow_reuse_address = True
    
    if type == "p":
        tipo_hijo = ForkedTCPServer
    
    elif type == "t":
        tipo_hijo = ThreadTCPServer

with tipo_hijo((HOST,PORT), MyTCPHandler) as server:
    server.serve_forever()