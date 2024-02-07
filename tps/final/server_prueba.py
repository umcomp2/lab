import socketserver
import argparse
import pickle
from celery_admin import *

analizador = argparse.ArgumentParser()
analizador.add_argument("-h", "--host", help="Host", type=str)
analizador.add_argument("-p", "--port", help="Port", type=int)
argumento = analizador.parse_args()

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            print('connection...')
            while True:
                data=self.request.recv(1024)
                if not data:
                    print('client disconnected...')
                    break

                print('pickle data: ',data)
                pickleD=pickle.loads(data)
                print('received: ',pickleD)
                if pickleD[0] == 'suma':
                    result=suma.delay(pickleD[1],pickleD[2])

                elif pickleD[0] == 'resta':
                    result=resta.delay(pickleD[1],pickleD[2])

                elif pickleD[0] == 'div':
                    result=div.delay(pickleD[1],pickleD[2])
                
                elif pickleD[0] == 'mult':
                    result=mult.delay(pickleD[1],pickleD[2])

                elif pickleD[0] == 'pot':
                    result=pot.delay(pickleD[1],pickleD[2])
                
                else:
                    print('sending data back to the client')
                    pickleM=pickle.dumps('operation was not selected')
                    self.request.sendall(pickleM)
                    exit()


                print('sending data back to the client')
                pickleM=pickle.dumps(result.get())
                self.request.sendall(pickleM)

        finally:
            self.request.close()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    import threading
    import signal

    HOST=argumento.host
    PORT=argumento.port
    dataServer=((HOST,PORT))

    server = ThreadedTCPServer(dataServer, MyTCPHandler)

    with server:
        ip, port = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        print("Server loop running:",ip,port)

        try:
            signal.pause()
        except:
            server.shutdown() 