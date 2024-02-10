import socketserver
from postgresql import connect_to_db;
import argparse
import threading
from celery_admin import *

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        
        cur_th = threading.get_native_id()
        tipo_usuario = self.request.recv(1024).strip()
        if tipo_usuario:
            print(f"Nuevo cliente conectado como {tipo_usuario}" + "Th: " + str(cur_th) )
            self.agregar_evento()
        else:
            print("Nuevo cliente conectado")

        while True:
            data = self.request.recv(1024).strip()
            if not data:
                print('Cliente desconectado...')
                break

            print(f"Mensaje recibido de hilo {cur_th}: {data}")
            
    def agregar_evento(self):
        # Aquí haces las preguntas necesarias para agregar un evento
        self.request.sendall(b"Ingrese el nombre del evento: ")
        nombre_evento = self.request.recv(1024).strip()

        self.request.sendall(bytes("Ingrese el número de sectores: ", 'utf-8'))
        num_sectores = int(self.request.recv(1024).strip())

        sectores = []
        for i in range(num_sectores):
            self.request.sendall(f"Ingrese el nombre del sector {i + 1}: ".encode())
            nombre_sector = self.request.recv(1024).strip().decode()
            self.request.sendall(f"Ingrese la capacidad del sector {i + 1}: ".encode())
            
            # Esperar la respuesta del cliente antes de enviar la siguiente pregunta
            capacidad_sector = self.request.recv(1024).strip()
            sectores.append({"nombre": nombre_sector, "capacidad": capacidad_sector})

        # Llama a la tarea de Celery para agregar el evento
        new_event.delay(nombre_evento, sectores)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="Dirección IP del servidor", type=str, default='localhost')
    parser.add_argument("-p", "--puerto", help="Puerto del servidor", type=int, default=9999)
    args = parser.parse_args()

    conexion_db = connect_to_db();

    server = socketserver.ThreadingTCPServer((args.ip, args.puerto), MyTCPHandler)
    print("Servidor iniciado. Esperando conexiones...")
    server.serve_forever()