import socketserver
import pickle
import subprocess
import argparse


class PickleRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            serial_cmd = self.request.recv(4096)
            data = pickle.loads(serial_cmd)
            
            if data == "bye":
                break
            
            command = data.split()
            returned = subprocess.run(command, capture_output=True)

            exit_code = bool(returned.returncode)

            if not exit_code:
                exit_stdout = str(returned.stdout, "utf-8")
                respuesta = pickle.dumps(f"OK\n{exit_stdout}")
            else:
                exit_stderr = str(returned.stderr, "utf-8")
                respuesta = pickle.dumps(f"ERROR\n{exit_stderr}")

            self.request.sendall(respuesta)
        return


# El orden en el que se heredan es importante!
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer, ):
    pass

class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer, ):
    pass


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999
    socketserver.TCPServer.allow_reuse_address = True

    parser = argparse.ArgumentParser()
    parser.add_argument("--address", type=str, default="0.0.0.0", help="Server IP")
    parser.add_argument("--port", type=int, default=9999, help="Server PORT")
    parser.add_argument("-m", "--multi", type=str, default="Single", help="Concurrency Mechanism")

    args = parser.parse_args()

    HOST = args.address
    PORT = args.port
    MULTI = args.multi

    if MULTI == "p":
        serverClass = ForkedTCPServer
    elif MULTI == "t":
        serverClass = ThreadedTCPServer
    else:
        serverClass = socketserver.TCPServer

    with serverClass((HOST, PORT), PickleRequestHandler) as server:
        server.serve_forever()