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

        horarios_disponibles = client_socket.recv(1024).decode()
        print(horarios_disponibles)

        selected_time = input("Selecciona un horario para reservar: ")
        client_socket.send(selected_time.encode())

        reserva_confirmada = client_socket.recv(1024).decode()
        print(reserva_confirmada)

    except ConnectionRefusedError:
        print("[ERROR] No se pudo conectar al servidor. Asegúrate de que el servidor esté en ejecución.")
    except BrokenPipeError:
        print("[ERROR] La conexión con el servidor se cerró inesperadamente.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    client()