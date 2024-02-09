import socketserver
import threading
import signal
import argparse

pars = argparse.ArgumentParser()
pars.add_argument("-i", "--ip", help="ip" , type=str)
pars.add_argument("-p", "--puerto", help="puerto", type=int)
args = pars.parse_args()


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
       while True:
            self.data = self.request.recv(1024).strip()
            if not self.data:
                print('Client disconnected...')
                break
            
            print(self.data)
            if self.data == b"admin":  # Note the "b" prefix for bytes literal
                self.request.sendall(b"SOS ADMIN")
            else:
                self.request.sendall(b"SOS USER")
            self.request.sendall(self.data.upper())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    
    socketserver.TCPServer.allow_reuse_address = True
    # Creo el server y bindeo a la ip y el puerto pasado por argumento

    with ThreadedTCPServer(('localhost', args.puerto), MyTCPHandler) as server:
        print("...Esperando nuevas conexiones...")
        server.serve_forever()
