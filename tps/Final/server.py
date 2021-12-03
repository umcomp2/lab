import argparse
import socketserver
import pickle
from tasks import *

parserito = argparse.ArgumentParser(description="Procesamiento de imagenes")

parserito.add_argument("-i", "--ip", dest="ip", help="ip", required=True)
parserito.add_argument("-p", "--puerto", dest="puerto",
                       help="Puerto", type=int, required=True)

args = parserito.parse_args()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(4096)
            if not data:
                break
            descerializado = pickle.loads(data)
            if descerializado[1] == "resaltar_luces":
                resultado = resaltar_luces.delay(descerializado[0], descerializado[2])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "contraste":
                resultado = contraste.delay(descerializado[0], descerializado[2])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "nitidez":
                resultado = nitidez.delay(descerializado[0], descerializado[2])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "tamaño":
                resultado = tamaño.delay(descerializado[0], descerializado[2], descerializado[3])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "recortar":
                resultado = recortar.delay(descerializado[0], descerializado[2], descerializado[3], descerializado[4], descerializado[5])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "texto":
                resultado = texto.delay(descerializado[0], descerializado[6])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "escala_grises":
                resultado = escala_grises.delay(descerializado[0])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "invertir_colores":
                resultado = invertir_colores.delay(descerializado[0])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "espejado":
                resultado = espejado.delay(descerializado[0])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "rotar_90":
                resultado = rotar_90.delay(descerializado[0])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "rotar_270":
                resultado = rotar_270.delay(descerializado[0])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "rotar_180":
                resultado = rotar_180.delay(descerializado[0])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "imagen_borrosa":
                resultado = imagen_borrosa.delay(descerializado[0])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "bordes":
                resultado = bordes.delay(descerializado[0])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            elif descerializado[1] == "enfocar":
                resultado = enfocar.delay(descerializado[0])
                serializador = bytes(resultado.get(), "utf-8")
                self.request.sendall(serializador)
            else:
                print('No existe esa edicion!')
                exit()

    


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