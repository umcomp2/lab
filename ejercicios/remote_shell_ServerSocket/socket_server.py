import socketserver
import subprocess
import pickle
import argparse

DISCONNECT_MESSAGE = b"\n---DESCONECTADO---"

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(conn, addr):
        print(f"---NUEVA CONEXIÓN---\n {addr} conectado con exito.")
    
        while True:
            msg = conn.recv(4096)       
            deserializado = pickle.loads(msg)
            if deserializado == DISCONNECT_MESSAGE:    
                break
            else:
                command = deserializado.split()
                process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                salida = pickle.dumps(stdout)
                error = pickle.dumps(stderr)
                conn.send(salida)
                conn.send(error)
class ThreadTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedTCPServer(socketserver.ForkingMixIn,socketserver.TCPServer):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SOCKET SERVER")
    parser.add_argument("-m", "--tipo", dest="tipo", required=True,help="forking o threading")
    args = parser.parse_args()

    HOST, PORT = "localhost", 9998
    if args.tipo.lower() == "p":
        tipo = ForkedTCPServer
    
    elif args.tipo.lower() == "t":
        tipo = ThreadTCPServer
    
    with tipo ((HOST, PORT), RequestHandler) as server:
        server.serve_forever()


