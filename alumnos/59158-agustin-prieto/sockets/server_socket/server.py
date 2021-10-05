#!/usr/bin/python3
import subprocess
import pickle
import socketserver
import argparse


FORMAT = 'utf-8'

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f'CONNECTION SUCCESFUL')
        connected = True
        while connected:
            data = self.request.recv(4096)
            message = pickle.loads(data)
            if message == b'exit':
                break
            out = subprocess.run(message.split(), capture_output=True)
            exit = bool(out.returncode)
            if exit == False:
                
                send_message = pickle.dumps(out.stdout) 
                self.request.send(send_message)
            
            else:
                error_message = pickle.dumps(out.stderr)
                self.request.send(error_message)





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port',action="store", type= int, required=True)
    parser.add_argument('-m', '--mode',action="store", required=True, type=str)
    args = parser.parse_args()
    PORT, MODE, HOST = args.port, args.mode, "localhost"

    if MODE == 't':
        server = ThreadedTCPServer((HOST, PORT), Handler)
    elif MODE == 'p':
        server = ForkedTCPServer((HOST, PORT), Handler)

    with server:
        server.serve_forever()



