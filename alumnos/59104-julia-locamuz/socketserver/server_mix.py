import os
import socketserver
import argparse
import threading
import pickle

forking_mode = False
threading_mode = False

parser2 = argparse.ArgumentParser()

parser2.add_argument('mode')
parser2.add_argument('-m', action='store_true')

args2 = parser2.parse_args()

if args2.m:
    mode = args2.mode
    if mode == 'p':
        forking_mode = True
        print("MULTIPLE CLIENTS --> forking mode activated")
    elif mode == 't': 
        threading_mode = True
        print("MULTIPLE CLIENTS --> threading mode activated")


class ForkingEchoRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            # Echo the back to the client
            data = self.request.recv(1024)
            msg_des = pickle.loads(data)
            print(msg_des)
            cur_pid = os.getpid()
            response = b'%d: %s' % (cur_pid, msg_des)
            msg_ser = pickle.dumps(response)
            self.request.send(msg_ser)



class ForkingEchoServer(socketserver.ForkingMixIn,socketserver.TCPServer,):
    pass



class ThreadedEchoRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Echo the back to the client
        while True:
            data = self.request.recv(1024)
            msg_des = pickle.loads(data)
            print(msg_des)
            cur_thread = threading.currentThread()
            response = b'%s: %s' % (cur_thread.getName().encode(),msg_des)
            msg_ser = pickle.dumps(response)
            self.request.send(msg_ser)

class ThreadedEchoServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass



if __name__ == '__main__':
    import threading
    # CREO OBJETO SERVER
    socketserver.TCPServer.allow_reuse_address = True
    address = ('localhost', 5050)  # let the kernel assign a port
    if forking_mode:
        
        server = ForkingEchoServer(address,ForkingEchoRequestHandler)
    elif threading_mode:
        server = ThreadedEchoServer(address,ThreadedEchoRequestHandler)
    else: 
        print("invalid mode")

    server.serve_forever()

    # Clean up
    server.socket.shutdown()
    server.socket.close()