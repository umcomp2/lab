import argparse
import socketserver
import pickle

parserito = argparse.ArgumentParser(description="Procesamiento de imagenes")

parserito.add_argument("-i", "--ip", dest="ip", help="ip", type=str)
parserito.add_argument("-p", "--puerto", dest="puerto",
                       help="Puerto", type=int, required=True)

args = parserito.parse_args()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(4000)
            if data == "exit":
                break
            descerializado = pickle.loads(data)



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    import threading
    import signal

    server = ThreadedTCPServer((args.ip, args.puerto), MyTCPHandler)

    with server:
        ip, puerto = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(f"direccion ip {ip} y puerto {puerto}")
        try:
            signal.pause()
        except:
            server.shutdown() 