import subprocess, socketserver, signal, os, pickle, argparse, sys
import socket as s


class MyConnectionHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("[+]CONEXION ESTABLECIDA DE {}:{}".format(self.client_address[0], self.client_address[1]))
        dir = pickle.dumps(os.getcwd())
        self.request.sendall(dir)
        while True:
            comando = self.request.recv(1024)
            comando2 = pickle.loads(comando)
            if comando2.lower() == "exit":
                print("\n[+]CONEXION FINALIZADA DE {}:{}".format(self.client_address[0], self.client_address[1]))
                break
            else:
                try:
                    output = subprocess.getoutput(comando2)
                    rta = f"OK\n{output}"
                except subprocess.CalledProcessError as error:
                    rta = f"ERROR\n{output}"
                self.request.sendall(pickle.dumps(rta))
            #self.data = self.request.recv(1024).strip()
            #print(self.data)
            #self.request.sendall(self.data.upper())
            #if self.data.decode() == 'exit':
            #    break

class ThreadTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="Serversocket with forking or threading")

        parser.add_argument("-m", "--mode", type=str, required=True, help="Type of mode (thread or fork)")

        parseo = parser.parse_args()
    except:
        print("Valores ingresados incorrectos")
        sys.exit()
    address = ('localhost', 9999)
    socketserver.TCPServer.allow_reuse_address = True

    if parseo.mode == 't':
        modo = ThreadTCPServer
        string = "Threading!"
    if parseo.mode == 'p':
        modo = ForkTCPServer
        string = "Forking!"
    with modo(address, MyConnectionHandler) as server:
        print(f"[+]SERVIDOR INICIADO! - {string}")
        #server_thread = threading.Thread(target=ThreadTCPServer, )
        server.serve_forever()
        try:
            signal.pause()
        except:
            server.shutdown()