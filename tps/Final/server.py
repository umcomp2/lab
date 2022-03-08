import argparse
import socketserver
import pickle
from tasks import *
from pymongo import MongoClient
import datetime

parserito = argparse.ArgumentParser(description="Procesamiento de imagenes")

parserito.add_argument("-i", "--ip", dest="ip", help="ip", required=True)
parserito.add_argument("-p", "--puerto", dest="puerto",
                       help="Puerto", type=int, required=True)

args = parserito.parse_args()


class MyTCPHandler(socketserver.BaseRequestHandler):
    # la funcion handle nos va a permitir que cuando se ejecute el servidor
    # quiero que la conexion con ese cliente se maneje de esta manera
    def handle(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client["images"]
        collection = db["edits"]
        dt = datetime.date.today()
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            descerializado = pickle.loads(data)
            resultado = funcion_generica.delay(descerializado)
            serializador = bytes(resultado.get(), "utf-8")
            self.request.sendall(serializador)
            dato_guardado = str(serializador, "utf-8")
            image = {f"edicion": descerializado[1],
                        "imagen_edit": dato_guardado,
                        "fecha": f"{dt.day}/{dt.month}/{dt.year}",
                        "nombre": descerializado[-1]}
            collection.insert_one(image)
                
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    import threading
    import signal

    server = ThreadedTCPServer((args.ip, args.puerto), MyTCPHandler)

    with server:
        ip, puerto = server.server_address
        # ejecuta handle en un bucle infinito
        server_thread = threading.Thread(target=server.serve_forever)
        # Lo seteamos en forma de demonio, es decir, que el hilo deamon pueda seguir
        # ejecutandonse mientras el principal hace otra cosa
        server_thread.daemon = True
        server_thread.start()
        print(f"direccion ip {ip} y puerto {puerto}")
        try:
            # Hacer que el proceso duerma hasta que se reciba una señal;
            # entonces se llamará al manejador apropiado. No devuelve nada.
            signal.pause()
        except:
            # nos permite cerrar el server y liberar el puerto
            server.shutdown()
