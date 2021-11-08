import subprocess
import pickle
import socketserver
import argparse


class EchoRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Nueva conexion establecida")
        connected  = True
        while connected:
            msg = self.request.recv(4096)
            msg = pickle.loads(msg)
            if msg == '!DISCONNECT':
                print(f"Conexion finalizada")
                break

            cmd = msg.split()
            estado_cmd = subprocess.run(cmd,capture_output=True)
            if estado_cmd.returncode == 0:
                correct_output = estado_cmd.stdout.decode("utf-8")
                msg_back = str(f"OK\n{correct_output}")
                msg_back = pickle.dumps(msg_back)
                self.request.send(msg_back)
            else:
                error_output = estado_cmd.stderr.decode("utf-8")
                msg_back = str(f"ERROR\n{error_output}")
                msg_back = pickle.dumps(msg_back)
                self.request.send(msg_back)
            
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer, ):
    pass

class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer, ):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port',action="store", type= int, required=True)
    parser.add_argument('-m', '--mode',action="store",choices=['p','t'], required=True, type=str)
    args = parser.parse_args()

    PORT = args.port
    SERVER = "127.0.0.1"
    MODE = args.mode

    if MODE == "p":
        serverClass = ForkedTCPServer
    elif MODE == "t":
        serverClass = ThreadedTCPServer
    
    with serverClass((SERVER, PORT), EchoRequestHandler) as server:
        server.serve_forever()