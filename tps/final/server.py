import argparse
import socket
import threading
from postgres import *
from celeryApp import *
import socketserver


def handleClient(client_socket):
    #le doy una conexion a cada cliente para que no se interfiera con otra conexion
    conexDB = conexionDB()
    client_address = client_socket.getpeername()
    #traigo los dias de la semana
    dias = getDias(conexDB)
    client_socket.send(str(dias).encode())
    dataDia = client_socket.recv(1024).decode().strip()
    selected_dia = dias[int(dataDia)]
    indiceDia_db = selected_dia[0]
    print("Dia elegido: \n", "-Id Dia: "+str(indiceDia_db), "\n-Dia Semana: " + str(selected_dia[1]))
    
    #traigo horarios
    while True:
        horario = getHorarios(conexDB)
        client_socket.send(str(horario).encode())
        dataHorario= client_socket.recv(1024).decode().strip()
        selected_hora = horario[int(dataHorario)]
        indiceHorario_db = selected_hora[0]
        print("Horario elegido: \n", "-Id Hora: "+str(indiceHorario_db), "\n-Dia Semana: " + str(selected_hora[1]))
    
    #veo disponibilidad en ese dia y horario

        disp = getDisponibilidad(conexDB, indiceDia_db, indiceHorario_db)
        # client_socket.send(str(disp).encode())
        lugares = int(disp[0])
        if lugares < 15:
            nuevo_valor = addCantidad(conexDB,indiceDia_db, indiceHorario_db)
            message = f"Si hay lugares disponibles\n"
            client_socket.sendall(message.encode())

            print("Lugares Ocupados: " + str(nuevo_valor))
            break
            #pedir nombre
        else:  
            client_socket.sendall(b"No hay lugares disponibles, elija otro!\n")  
    
    client_socket.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #vincula el host con el puerto
    server.bind((host, port))
    server.listen(5)
    print(f"[INFO] Servidor escuchando en {host}:{port}...")

    while True:
        client_socket, _ = server.accept()
        print(f"[INFO] Conexión establecida desde {client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}")
        client_handler = threading.Thread(target=handleClient, args=(client_socket,))
        client_handler.start()
        




# def getDias():
#     dias = getDiasSemana.delay().get()
#     return dias

# def enviarDias(self, dias):
#     diasSemana = "\n".join([f"{dia['id']}: {dia['dia_semana']}\n" for d in dias])
#     self.request.sendall(diasSemana.encode())





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #declaro los args para la conexion
    parser.add_argument("-i", "--ip", help="ip", type=str)
    parser.add_argument("-p", "--port", help="port", type=int)
    args = parser.parse_args()
    conexDB = conexionDB()
    # if conexDB:
    #     crear_tablas(conexDB)
    #     conexDB.close()
    start_server(args.ip, args.port)

   

# def enviarDias(self, dias):
#     dia_str = "\n".join([f"{diaS['id']}: {evento['nombre']}\n" for evento in eventos])
#     self.request.sendall()

# def reservarTurno(self):
    
    # self.request.sendall(b"Ingrese su nombre: ")
    # nombreCliente = self.request.recv(1024).strip().decode("utf-8")
    # self.request.sendall(b"Ingrese su dni: ")
    # dniCliente = int(self.request.recv(1024).strip())
