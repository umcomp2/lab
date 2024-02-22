import argparse
import socket
import pickle


def client():

    parser = argparse.ArgumentParser()
    #declaro los args para la conexion
    parser.add_argument("-i", "--ip", help="ip", type=str)
    parser.add_argument("-p", "--port", help="port", type=int)

    args = parser.parse_args()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    try:
        #creacion el socket

        client_socket.connect((args.ip, args.port))
        print(f"[INFO] Conexión establecida con el servidor PILATES UMA en {args.ip}:{args.port}")
        #string de datos de dias disponibles
        print("\n---!BIENVENIDO A NUESTRO SISTEMA DE RESERVA DE TURNOS!---")
        print("\nDIAS DE LA SEMANA DISPONIBLES:")
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
        while True:
        #string de horarios de dias disponibles
            print("\nHORARIOS DE LA SEMANA DISPONIBLES: ")
            horarios_disponibles = client_socket.recv(1024).decode()
            listaHorarios = eval(horarios_disponibles)
            for index, hora in enumerate(listaHorarios):
                print(str(index+1) + "-" + str(hora[1]))
            validate = True

            while validate:
                try: 
                    selected_hora = int(input("Seleccione el indice del horario: "))-1
                    listaHorarios[(selected_hora)]
                    validate = False
                except:
                    print("Indice incorrecto")

            client_socket.send(str(selected_hora).encode())
            

            #veo disponibilidad
            mensajeDisponibilidad = client_socket.recv(1024).decode()
            if mensajeDisponibilidad.startswith("Si hay"):
                print(mensajeDisponibilidad)
                break
            print(mensajeDisponibilidad)

        #Pedimos datos personales para completar la reserva    
        preguntaNombre = client_socket.recv(1024).decode()
        respuestaNombre = input(preguntaNombre)
        client_socket.send(str(respuestaNombre).encode())

        preguntaDni = client_socket.recv(1024).decode()
        respuestaDni = input(preguntaDni)
        client_socket.send(str(respuestaDni).encode())

        listaReserva = client_socket.recv(4096)
        receivedList = pickle.loads((listaReserva))
        print("\nRESERVA CONFIRMADA: ")
        for reserva in receivedList:
            print("Nombre:", reserva['Nombre'])
            print("DNI:", reserva['Dni'])
            print("Día:", reserva['Dia'])
            print("Horario:", reserva['Horario'])
            print()  
        


    except ConnectionRefusedError:
        print("[ERROR] No se pudo conectar al servidor. Asegúrate de que el servidor esté en ejecución.")
    except BrokenPipeError:
        print("[ERROR] La conexión con el servidor se cerró inesperadamente.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    client()