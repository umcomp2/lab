import socket, os, threading, datetime

MAX_SIZE=512
KEY="12135"

TODAY=datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

'''Crear un cliente.py que reciba por argumento:
    -h host -> analytics.juncotic.com
    -p port -> 2222
    Protocolo:
            -> hello|diego
            <- cod
            -> email|diego@juncotic.com
            <- cod
            -> key|XXXXX
            <- cod
            -> exit
            <- cod
    Respuestas:
            200 -> OK
            400 -> Comando incorrecto
            404 -> Clave invalida
            500 -> Sale sin autenticar (exit)'''

def th_server(sock_full):
    name = "_"
    key="_"
    email="_"
    sock,addr = sock_full
    print("Launching thread... addr: %s" % str(addr))
    exit = False
    ip=str(addr)
    # pasos del protocolo
    stage = 0
    while True:
        # me quedo escuchando por el socket algo del cliente
        msg = sock.recv(MAX_SIZE).decode()
        print("Recibido: %s" % msg)
        # verifico si es hello el comando
        if msg[0:5] =="hello":
            # solo se ejecuta si estamos en la etapa 0
            if stage == 0:
                # guardo el nombre
                name = msg[6:]
                # codigo de respueta exitosa
                resp = "200"
                # avanzo a la siguiente etapa
                stage += 1
            else:
                # sino el codigo de error de comando incorrecto
                # no avanzo de etapa, asi vuelve a lupear en el nombre
                resp = "400"
        # una vez que pone el nombre bien pide el email
        elif msg[0:5] == "email":
            # recibe el mail del servidor si estamos en la etapa 1
            email = msg[6:]
            if stage==1:
                email = msg[6:]
                resp = "200"
                stage+=1
            else:
                resp = "400"
        # pasamos a la clave
        elif msg[0:3] == "key":
            if stage==2:
                key = msg[4:]
                # comparo la clave del cliente con al del servidor
                if key != KEY:
                    print(key)
                    # si esta mal respondo con un error de clave invalida
                    resp="404"
                else:
                    resp = "200"
                    stage+=1
            else:
                resp = "400"
        # comando exit para salir
        # lo pueden tirar en cualquier etapa del protocolo que va a salir
        elif msg[0:4] == "exit":
            resp = "200"
            exit = True
        else:
            # error de salir sin autentificar por que el programa termina igual
            resp = "500"
        # respondo al cliente con el codigo de respuesta cargado
        sock.send(resp.encode("ascii"))
        if exit:
            # si autentifico muestro la linea por pantalla de que se establecio la conexion
            data = "%s|%s|%s|%s|%s" % (TODAY,name,email,key,ip)
            data = data.replace('\n', '').replace('\r', '')
            print(data)
            sock.close()
            break
            

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# para no tener que ir cambiando el puerto que no este en uso
# esta linea lo que hace es que si el puerto no esta en uso, limpialo y usalo de vuelta 
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# get local machine name
#host = socket.gethostname()
# "" signfica que atiendo en todas las ip de la maquina
host = ""
port= 2222

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket = serversocket.accept()

    print("Got a connection from %s" % str(clientsocket[1]))

    # msg = 'Thank you for connecting'+ "\r\n"
    # clientsocket[0].send(msg.encode('ascii'))
    # por cada cliente aceptado lanzo un thread
    th = threading.Thread(target=th_server, args=(clientsocket,))
    th.start()
