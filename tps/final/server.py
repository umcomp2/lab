import socketserver
from postgresql import connect_to_db;
import argparse
import threading

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        
        cur_th = threading.get_native_id()
        tipo_usuario = self.request.recv(1024).strip()
        if tipo_usuario:
            print(f"Nuevo cliente conectado como {tipo_usuario}" + "Th: " + str(cur_th) )
        else:
            print("Nuevo cliente conectado")

        while True:
            data = self.request.recv(1024).strip()
            if not data:
                print('Cliente desconectado...')
                break

            print(f"Mensaje recibido de hilo {cur_th}: {data}")
            # respuesta = self.procesar_mensaje(tipo_usuario, data)
            self.request.sendall(data.upper())

            # self.request.sendall(respuesta.encode())

    def procesar_mensaje(self, tipo_usuario, mensaje):
        if tipo_usuario.lower() == "admin":
            return f"Acción de administrador: {mensaje.upper()}"
        else:
            return f"Acción de usuario: {mensaje.lower()}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="Dirección IP del servidor", type=str, default='localhost')
    parser.add_argument("-p", "--puerto", help="Puerto del servidor", type=int, default=9999)
    args = parser.parse_args()

    conexion_db = connect_to_db();

    server = socketserver.ThreadingTCPServer((args.ip, args.puerto), MyTCPHandler)
    print("Servidor iniciado. Esperando conexiones...")
    server.serve_forever()