import socketserver
import argparse
import pickle
from tasks import *

parser = argparse.ArgumentParser(description = "Calculadora remota con Celery" )

parser.add_argument("-i", "--ip", dest="ip", help="ip", type=str)
parser.add_argument("-p", "--puerto", dest = "puerto",help="Puerto", type=int)
args = parser.parse_args()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        connected = True
        while connected:
            data = self.request.recv(1024)
            if data == "exit":
                break
            descerializado = pickle.loads(data)
            if descerializado[0] == 'suma':
                    resultado=suma.delay(descerializado[1],descerializado[2])

            elif descerializado[0] == 'resta':
                resultado=resta.delay(descerializado[1],descerializado[2])

            elif descerializado[0] == 'div':
                resultado=div.delay(descerializado[1],descerializado[2])
            
            elif descerializado[0] == 'mult':
                resultado=mult.delay(descerializado[1],descerializado[2])

            elif descerializado[0] == 'pot':
                resultado=pot.delay(descerializado[1],descerializado[2])
            
            else:
                print('Operación no existente')
                exit()
        serializador = pickle.dumps(resultado.get())
        self.request.sendall(serializador)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    import threading
    import signal

    HOST=args.ip
    PORT=args.puerto
    descerializadoServer=((HOST,PORT))

    server = ThreadedTCPServer(descerializadoServer, MyTCPHandler)

    with server:
        ip, puerto = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        print("[SERVER RUNNING]",ip,puerto)

        try:
            signal.pause()
        except:
            server.shutdown() 