import socket
import subprocess
import signal


def handler(signum, frame):
    server_socket.close()
    exit(0)

# Para el cierre del server
signal.signal(signal.SIGINT, handler)

# Obtener de forma simple por CLI 
# ip y puerto al que voy a unir el servidor
HOST = 'localhost'
PORT = 8000

# Crear objeto socket del lado del server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Establecemos el socket para escuchar en [HOST] y [PORT]
server_socket.bind((HOST, PORT))
# socket.listen([backlog])
# El backlog es la cantidad de conexiones que puede tener en espera
# para hacer el SYN-SYN/ACK-ACK
# cuando el cliente se conecta y se producia el hansheik 
# syns, syns ask, ask para comenzar a transferir informacion
# estos 3 pasos permite a los dos procesos establecer la conexion
# a partir de ahi tenemos todos los numeros de secuencia y de acnolich
# cuando un cliente hace conect hay un lazo de tiempo entre ese conect hasta que es aceptada
# mientras todavia no se producen los tres mensajes del hanshake la conecion esta inacectada
# entonces es el numero de conecciones pendientes de su hanshake antes que se sean aceptadas
# y al resto le hace drop entonces funciona como un control de negacion de servicio
server_socket.listen(2)
# el bucle para que pueda recibir conexiones de clientes
while True:
# El conector debe estar vinculado a una dirección y escuchando conexiones
# El valor de retorno es un par (conexión, dirección)
# donde conn es un nuevo objeto de socket que se puede usar para enviar y recibir datos en el
# conexión, y la dirección es la dirección vinculada al zócalo en el otro
# fin de la conexión. 
    conn, addr = server_socket.accept()
    print(f"Nueva conexion desde {addr}...")

    while conn:
        # recive del cliente y lo codea a stream
        data = str(conn.recv(4096), "utf-8")
        # separo en una lista con cada palabra del comando como elemento de esa lista para poder ejecutarlos
        command = data.split()
        # me retorna un objeto de proceso completado
        returned = subprocess.run(command, capture_output=True)
        # aca leo los atributos y lo paso a boleano para poder determinar si es error o no
        exit_code = bool(returned.returncode)
        # lo que sale en el standar ouput y el standar error
        if not exit_code:
            # codeo a stream
            exit_stdout = str(returned.stdout, "utf-8")
            # asigno una respuesta al ouput del comando
            respuesta = bytes(f"OK\n{exit_stdout}", "utf-8")
        else:
            exit_stderr = str(returned.stderr, "utf-8")
            # asigno una respuesta de error al ouput del cliente
            respuesta = bytes(f"ERROR\n{exit_stderr}", "utf-8")
        # envio la respuesta al cliente
        conn.send(respuesta)
    # itera hasta que el cliente ingrese el comando exit
    conn.close()
