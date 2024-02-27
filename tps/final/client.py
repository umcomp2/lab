import argparse
import socket
import pickle
import time


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
        print("\n---!BIENVENIDO A NUESTRO SISTEMA DE RESERVA DE TURNOS!---\nESTAS SON NUESTRAS ACTIVIDADES:")
        validateActividad= True
        while validateActividad:
            print("\n1.SACAR TURNO\n2.CANCELAR TURNO\n3.SALIR DEL SISTEMA")
            opcion = int(input("\nSeleccione el indice de una de las actividades: "))
            client_socket.send(str(opcion).encode())
            if opcion == 1:
                
                print("\nUSTED HA ELEIGO LA ACTIVIDAD SACAR TURNO\n")
                time.sleep(1)
                validateOpcion1 = True
                while validateOpcion1:
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
                
                #string de horarios de dias disponibles
                    time.sleep(1)
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
                        # print(mensajeDisponibilidad)
                        validateOpcion1 = False
                    else:
                        print("---- "+mensajeDisponibilidad+" ----")
                time.sleep(1)
                #Pedimos datos personales para completar la reserva    
                preguntaNombre = client_socket.recv(1024).decode()
                respuestaNombre = input(preguntaNombre)
                client_socket.send(str(respuestaNombre).encode())
                time.sleep(1)
                preguntaDni = client_socket.recv(1024).decode()
                respuestaDni = input(preguntaDni)
                dniSinPuntos = respuestaDni.replace('.', '')
                client_socket.send(str(dniSinPuntos).encode())
               
                    
                listaReserva = client_socket.recv(4096)
                receivedList = pickle.loads((listaReserva))
                
                print("\nRESERVA CONFIRMADA: ")
                for reserva in receivedList:
                    print("Nombre:", reserva['Nombre'])
                    print("DNI:", reserva['Dni'])
                    print("Día:", reserva['Dia'])
                    print("Horario:", reserva['Horario'])
                    print()  
                validateActividad = False
            if opcion == 2:
                
                print("\nUSTED HA ELEIGO LA OPCION CANCELAR TURNO\n")
                n = True
                while n:
                #1. pido y mando dni
                    time.sleep(1)
                    dni = str(input("Porfavor ingrese su dni para ver sus turnos: "))
                    dniSinPuntos = dni.replace('.', '')
                    client_socket.send(str(dniSinPuntos).encode())
                    #2. Recibo si existe o no el dni
                    existe = client_socket.recv(1024).decode()
                    # print("existe?: " + existe)
                     #2.1 existe dni?
                    if existe == "True": 
                        #3.1 recibo las reseervas del servidor
                        turno = client_socket.recv(1024).decode()
                        listaTurnos = eval(turno)
                        # print(listaTurnos)
                        time.sleep(1)
                        print("\n"+str(listaTurnos[0][4]).upper()+" ESTOS SON TUS TURNOS:")
                        for index, t in enumerate(listaTurnos):
                                print(str(index+1) + "-" +"Dia: " +str(t[2])+ " -" +"Hora: " +str(t[1]))

                        validate = True
                        #El cliente elige el turno para eliminar
                        while validate:
                            try: 
                                selected_turno = int(input("\nSeleccione el indice del turno que quiera eliminar: "))-1
                                idReserva = listaTurnos[selected_turno][0]
                                listaTurnos[(selected_turno)]
                                validate = False
                            except:
                                print("Indice incorrecto. Elija otro")
                        #4. cliente manda el indie de reserva
                        client_socket.send(str(idReserva).encode())
                        respuestaCancelacion = client_socket.recv(1024).decode()
                        print(respuestaCancelacion)
                        n=False

                    else: 
                        print("Dni invalido. Seleccione otro!")
                validateActividad = False
  

            if opcion == 3:
                # print("\nUsted va a salir del sistema! Que tenga buen dia!")
                validateActividad = False


            # else:
            #     print("Esa no es una opcion!, Elegir otra..")
    except ConnectionRefusedError:
        print("[ERROR] No se pudo conectar al servidor. Asegúrate de que el servidor esté en ejecución.")
    except BrokenPipeError:
        print("[ERROR] La conexión con el servidor se cerró inesperadamente.")
    finally:
        
        print("\nGracias por utilizar nuestro servicio de reservas!")
        time.sleep(1)
        client_socket.close()

if __name__ == "__main__":
    client()