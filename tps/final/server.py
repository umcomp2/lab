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
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()

        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    import socket

    socketserver.TCPServer.allow_reuse_address = True
    # Creo el server y bindeo a la ip y el puerto pasado por argumento

    server = ThreadedTCPServer((args.ip, args.puerto), MyTCPHandler)

    t = threading.Thread(target=server.serve_forever)
    # t.setDaemon(True)  # don't hang on exit
    t.start()

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.ip, args.puerto))
