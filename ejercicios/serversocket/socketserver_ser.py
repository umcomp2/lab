import socketserver as ss
import subprocess as sp
import pickle
import argparse


class RequestHandler(ss.BaseRequestHandler):

    def handle(self):
        print("Conexion establecida")
        while True:

            data = self.request.recv(4096)
            data2 = pickle.loads(data)

            if data2 != "exit":
                datos = data2.split()
                fin = sp.Popen(datos, stdout=sp.PIPE, universal_newlines=True, stderr=sp.PIPE)
                output_full = fin.communicate()
                salida = pickle.dumps(output_full[0])
                error = pickle.dumps(output_full[0])
                self.request.send(salida)
                self.request.send(error)
            
            elif data2 == "exit":
                break
            
class ThreadedTCPServer(ss.ThreadingMixIn, ss.TCPServer, ):
    pass

class ForkedTCPServer(ss.ForkingMixIn, ss.TCPServer, ):
    pass

if __name__ == "__main__":
    parserito_s = argparse.ArgumentParser(description='socket server')
    parserito_s.add_argument('-p', '--port', dest = "puerto", type = int, required = True, help = "Puerto utilizado")
    parserito_s.add_argument('-m', '--tipo', dest = "tipo", required = True, help = "tipo de miltiprocesamiento")

    args = parserito_s.parse_args()

    id = "0.0.0.0"

    if args.tipo.lower() == "p":
        serverClass = ForkedTCPServer

    elif args.tipo.lower() == "t":
        serverClass = ThreadedTCPServer
    
    with serverClass((id, args.puerto), RequestHandler) as server:
        server.serve_forever()
