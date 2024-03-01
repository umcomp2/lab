import socketserver
from postgresql_config import connect_to_db;
import argparse
import threading
from celery_admin import *
import time
import pickle
import socket

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="Dirección IP del servidor", type=str)
parser.add_argument("-p", "--puerto", help="Puerto del servidor", type=int, default=9999)
parser.add_argument("-pr", "--protocolo", help="Ipv4 o Ipv6", type=int, default=9999)

args = parser.parse_args()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        
        client_ip = self.client_address[0]
        cur_th = threading.get_native_id()
        tipo_usuario = self.request.recv(1024).strip().decode()
        print(f"Nuevo cliente conectado como {tipo_usuario} Th: {cur_th} IP: {client_ip}")

        if tipo_usuario == 'admin':
            respuesta_si_no_serilizada = self.request.recv(1024)
            respuesta_si_no_descerializada = pickle.loads(respuesta_si_no_serilizada)
            if respuesta_si_no_descerializada == 1:
                time.sleep(1)
                print("----Agregando evento----")
                msg = self.agregar_evento()
                print("----"+ msg +"----")
                self.request.sendall(msg.encode())
            
            else:
                eventos = self.obtener_eventos()
                self.enviar_eventos(eventos)
                self.request.sendall(b"Escriba el numero del evento que desea eliminar:")
                respuesta = self.request.recv(1024).strip().decode()
                msj_task = self.borrar_evento(respuesta)
                self.request.sendall(msj_task.encode())


        else:
            self.request.sendall(b"- Presione 1 para ver eventos disponibles \n - Presione 2 para ver sus compras")
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

                    self.request.sendall(b"\nIngrese el nombre correctamente del sector que desea comprar: ")
                    nombre_sector = self.request.recv(1024).strip().decode()
                    self.request.sendall(b"Ingrese la cantidad de entradas que desea comprar: ")
                    cantidad_entradas = int(self.request.recv(1024).strip().decode())
                    self.request.sendall(b"Ingrese su numero de documento")
                    numero_dni = int(self.request.recv(1024).strip().decode())
                    print(numero_dni)
                    mensaje_respuesta = self.comprar_entradas(id_evento, nombre_sector, cantidad_entradas, numero_dni)
                    self.request.sendall(mensaje_respuesta.encode())

                    # Preguntar si desea realizar otra compra
                    self.request.sendall(b"Desea realizar otra compra? (si/no): ")
                    respuesta = self.request.recv(1024).strip().decode()
                    if respuesta.lower() != 'si':
                        self.request.sendall(b"Gracias por su compra!")
                        break 
                    
            else:
                contador = 0
                while contador == 0:
                    self.request.sendall(b"Ingrese su numero de DNI: ")
                    dni = self.request.recv(1024).strip().decode()
                    print(f"----- Buscando compras para DNI: {dni} -----")
               
                    compras = buscar_compras_por_dni.delay(dni).get()
                    try:
                        if compras:
                            mensajes = []
                            for compra in compras:
                                evento_nombre, sector_nombre, cantidad_entradas = compra
                                mensaje_respuesta = f"Evento: {evento_nombre.upper()} - Sector: {sector_nombre} - Entradas compradas {cantidad_entradas} \n"  
                                mensajes.append(mensaje_respuesta)
                            mensajes_concatenados = ''.join(mensajes) 
                            self.request.sendall(mensajes_concatenados.encode())
                            self.request.sendall(b"Gracias por su compra!")
                            contador = 1
                            # self.request.close()
                    except:
                        self.request.sendall(b"No se encontraron compras para el DNI proporcionado.")

        while True:
            data = self.request.recv(1024).strip()
            if not data:
                print(f'Cliente th_id: {cur_th} desconectado...')
                break

            print(f"Mensaje recibido de hilo {cur_th}: {data}")
            
    def agregar_evento(self):
        
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
        
        evento = new_event.delay(nombre_evento, sectores).get()
        return evento
        

           
    def obtener_eventos(self):
        eventos = get_events.delay().get()
        return eventos

    def enviar_eventos(self, eventos):
        # Enviar eventos al cliente
        eventos_str = "".join([f"{evento['id']}: {evento['nombre']}\n" for evento in eventos])
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
    
    def borrar_evento(self, evento_id):
        msj_respuesta = delete_event.delay(evento_id).get()
        return msj_respuesta
    
class ThreadTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6
    pass

class ThreadTCPServerIPV4(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":

    conexion_db = connect_to_db();
    if args.protocolo == 4:
        server = ThreadTCPServerIPV4(("10.188.154.219", args.puerto), MyTCPHandler)
    else:
        server = ThreadTCPServer(("::1", args.puerto), MyTCPHandler)  
    print("Servidor iniciado. Esperando conexiones...")
    server.serve_forever()
     
# Escuchar en IPv4
    # server_ipv4 = ThreadTCPServerIPV4(("0.0.0.0", 2701), MyTCPHandler)
    # ipv4_thread = threading.Thread(target=server_ipv4.serve_forever)
    # # ipv4_thread.daemon = True
    # # ipv4_thread.start()
    # print("Servidor iniciado. Esperando conexiones...")

    # server_ipv4.serve_forever()

    # # Escuchar en IPv6
    # server_ipv6 = ThreadTCPServer(("::", 2702), MyTCPHandler)
    # ipv6_thread = threading.Thread(target=server_ipv6.serve_forever)
    # # ipv6_thread.daemon = True
    # # ipv6_thread.start()
    # server_ipv6.serve_forever()

    # print("Servidor iniciado. Esperando conexiones...")

    