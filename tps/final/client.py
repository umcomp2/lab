import argparse
import socket
import time
import sys

def client():

    parser = argparse.ArgumentParser()
    #declaro los args para la conexion
    parser.add_argument("-i", "--ip", help="ip", type=str)
    parser.add_argument("-p", "--port", help="port", type=int)
    parser.add_argument("-n", "--name", help="name", type=str)

    args = parser.parse_args()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    try:
        #creacion el socket

        client_socket.connect((args.ip, args.port))
        print(f"[INFO] Conexión establecida con el servidor en {args.ip}:{args.port}")
        #string de datos de dias disponibles
        dias_disponibles = client_socket.recv(1024).decode()
        listaDias= eval(dias_disponibles)
        for index, dia in enumerate(listaDias):
            print(str(index+1) + "-" + str(dia[1]))
        validate = True

        while validate:
            try: 
                selected_dias = int(input("Seleccione el indice del dia: "))-1
                listaDias[(selected_dias)]
                validate = False
            except:
                print("Indice incorrecto") 
                
        client_socket.send(str(selected_dias).encode())

        #string de horarios de dias disponibles
        horarios_disponibles = client_socket.recv(1024).decode()
        listaHorarios = eval(horarios_disponibles)
        for index, hora in enumerate(listaHorarios):
            print(str(index+1) + "-" + str(hora[1]))
        validate = True

        while validate:
            try: 
                selected_hora = int(input("Seleccione el indice del horario: "))-1
                listaDias[(selected_hora)]
                validate = False
            except:
                print("Indice incorrecto")

        client_socket.send(str(selected_hora).encode())

        #traigo disponibilidad
        disp = client_socket.recv(1024).decode()
        listaDisp = eval(disp)
        print("disponibilidad para ese dia y horario: " + str(listaDisp[0]))
        #client_socket.send(str(selected_hora).encode())

        # for index, lugar in enumerate(listaDisp):
        #     print(str(index+1) + "-" + str(lugar[1]))


        # reserva_confirmada = client_socket.recv(1024).decode()
        # print(reserva_confirmada)

    except ConnectionRefusedError:
        print("[ERROR] No se pudo conectar al servidor. Asegúrate de que el servidor esté en ejecución.")
    except BrokenPipeError:
        print("[ERROR] La conexión con el servidor se cerró inesperadamente.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    client()