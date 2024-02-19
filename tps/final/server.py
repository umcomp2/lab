import socketserver
from postgresql_config import connect_to_db;
import argparse
import threading
from celery_admin import *
import time


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        
        cur_th = threading.get_native_id()
        tipo_usuario = self.request.recv(1024).strip().decode()
        print(f"Nuevo cliente conectado como {tipo_usuario}" + " Th: " + str(cur_th) )

        if tipo_usuario == 'admin':
                print("----Agregando evento----")
                time.sleep(3)
                self.agregar_evento()
            
        else:
            self.request.sendall(b"Presione 1 para ver eventos \n - Presione 2 para ver compras")
            respuesta = self.request.recv(1024).strip().decode()
            if respuesta == "1":
                while True:
                    eventos = self.obtener_eventos()
                    print("---Buscando eventos---")
                    time.sleep(3)
                    print("---Eventos encontrados---")
                    self.enviar_eventos(eventos)
                    self.request.sendall(b"Ingrese el nro del evento que desee ver las entradas disponibles: ")
                    id_evento = self.request.recv(1024).strip().decode()
                    print("---Buscando entradas disponibles---")
                    sectores = self.obtener_sectores(id_evento)
                    self.enviar_sectores(sectores)
                    print("---Entradas disponibles encontradas---\n")

                    self.request.sendall(b"\nIngrese el nombre del correctamente del sector que desea comprar: ")
                    nombre_sector = self.request.recv(1024).strip().decode()
                    self.request.sendall(b"Ingrese la cantidad de entradas que desea comprar: ")
                    cantidad_entradas = int(self.request.recv(1024).strip().decode())
                    self.request.sendall(b"Ingrese su numero de documento")
                    numero_dni = int(self.request.recv(1024).strip().decode())
                    mensaje_respuesta = self.comprar_entradas(id_evento, nombre_sector, cantidad_entradas, numero_dni)
                    self.request.sendall(mensaje_respuesta.encode())

                    # Preguntar si desea realizar otra compra
                    self.request.sendall(b"Desea realizar otra compra? (si/no): ")
                    respuesta = self.request.recv(1024).strip().decode()
                    if respuesta.lower() != 'si':
                        break  # Salir del ciclo de compras
            else:
                self.request.sendall(b"Ingrese su numero de DNI: ")
                respuesta_dni = self.request.recv(1024).strip().decode()
                compras = self.obtener_compras(respuesta_dni)
                self.enviar_compras(compras)

        while True:
            data = self.request.recv(1024).strip()
            if not data:
                print('Cliente desconectado...')
                break

            print(f"Mensaje recibido de hilo {cur_th}: {data}")
            
    def agregar_evento(self):
        # Aquí haces las preguntas necesarias para agregar un evento
        self.request.sendall(b"Ingrese el nombre del evento: ")
        nombre_evento = self.request.recv(1024).strip().decode("utf-8")

        self.request.sendall(b"Ingrese el numero de sectores: ")

        num_sectores = int(self.request.recv(1024).strip())

        sectores = []
        for i in range(num_sectores):
            self.request.sendall(f"Ingrese el nombre del sector {i + 1}: ".encode())
            nombre_sector = self.request.recv(1024).strip().decode()
            self.request.sendall(f"Ingrese la capacidad del sector {i + 1}: ".encode())
            
            # Esperar la respuesta del cliente antes de enviar la siguiente pregunta
            capacidad_sector = int(self.request.recv(1024).strip())
            sectores.append({"nombre": nombre_sector, "capacidad": capacidad_sector})

        new_event.delay(nombre_evento, sectores)
           
    def obtener_eventos(self):
        eventos = get_events.delay().get()
        return eventos

    def enviar_eventos(self, eventos):
        # Enviar eventos al cliente
        eventos_str = "\n".join([f"{evento['id']}: {evento['nombre']}\n" for evento in eventos])
        self.request.sendall(eventos_str.encode())

    def obtener_sectores(self, evento_id):
        sectores = get_sectores.delay(evento_id).get()
        return sectores

    def enviar_sectores(self, sectores):
        sectores_str = "\n".join([f"{sector['nombre']}: Entradas disponibles:  {sector['capacidad']} " for sector in sectores])
        self.request.sendall(sectores_str.encode())

    def comprar_entradas(self, evento_id, nombre_sector, cantidad_entradas, dni):
        mensaje_respuesta = comprar_entradas.delay(evento_id, nombre_sector, cantidad_entradas, dni).get()
        return mensaje_respuesta
    
    def obtener_compras(self, dni):
        eventos = get_events.delay().get()
        compras = buscar_compras_por_dni.delay(dni, eventos)
        return compras
    
    def enviar_compras(self, compras):
        for evento, detalles_compras in compras:
            mensaje_evento = f"Eventos: {evento}\n"
            self.request.sendall(mensaje_evento.encode())

            for detalle_compra in detalles_compras:
                mensaje_compra = f"Detalles de la compra: {detalle_compra}\n"
                self.request.sendall(mensaje_compra.encode())

        # # Una vez que se han enviado todos los datos, puedes enviar una señal de finalización
        # mensaje_fin = "FIN\n"
        # cliente_socket.sendall(mensaje_fin.encode())



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="Dirección IP del servidor", type=str, default='localhost')
    parser.add_argument("-p", "--puerto", help="Puerto del servidor", type=int, default=9999)
    args = parser.parse_args()

    conexion_db = connect_to_db();

    server = socketserver.ThreadingTCPServer((args.ip, args.puerto), MyTCPHandler)
    print("Servidor iniciado. Esperando conexiones...")
    server.serve_forever()