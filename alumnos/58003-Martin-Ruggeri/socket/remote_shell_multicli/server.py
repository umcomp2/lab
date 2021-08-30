import socket
import sys
import subprocess
import concurrent.futures as cf


def recv_conn(conn, addr):
    while conn:
        data = str(conn.recv(4096), "utf-8")
        command = data.split()
        returned = subprocess.run(command, capture_output=True)
        exit_code = bool(returned.returncode)

        if not exit_code:
            exit_stdout = str(returned.stdout, "utf-8")
            respuesta = bytes(f"OK\n{exit_stdout}", "utf-8")
        else:
            exit_stderr = str(returned.stderr, "utf-8")
            respuesta = bytes(f"ERROR\n{exit_stderr}", "utf-8")

        conn.send(respuesta)

    conn.close()
    print(f"Conexion con {addr} finalizada...")


# Obtener de forma simple por CLI 
HOST = "127.0.0.1"
PORT = int(sys.argv[1])

# Crear objeto socket del lado del server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Creamos un pool de trabajadores para servir a las conexiones entrantes
pool = cf.ThreadPoolExecutor()

# Establecemos el socket para escuchar en [HOST] y [PORT]
server_socket.bind((HOST, PORT))
# socket.listen([backlog])
# El backlog es la cantidad de conexiones que puede tener en espera
# para hacer el SYN-SYN/ACK-ACK
server_socket.listen()

while True:
# socket.accept()
# Acepta una conexión. El socket debe estar vinculado a una dirección y escuchando conexiones
# El valor de retorno es un par (conexión, dirección)
# donde conn es un nuevo objeto de socket que se puede usar para enviar y recibir datos en el
# conexión, y la dirección es la dirección vinculada al zócalo en el otro
# final de la conexión.
    conn, addr = server_socket.accept()
    print(f"Nueva conexion desde {addr}...")
    pool.submit(recv_conn, conn, addr)
