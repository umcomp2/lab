import socket
import sys
import subprocess
import signal


def handler(signum, frame):
    server_socket.close()
    exit(0)

# Para el cierre del server
signal.signal(signal.SIGINT, handler)

# Obtener de forma simple por CLI 
HOST = "127.0.0.1"
PORT = int(sys.argv[1])

# Crear objeto socket del lado del server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Establecemos el socket para escuchar en [HOST] y [PORT]
server_socket.bind((HOST, PORT))
server_socket.listen(0)

while True:
# socket.accept()
# Accept a connection. The socket must be bound to an address
# and listening for connections. The return value is a pair (conn, address)
# where conn is a new socket object usable to send and receive data on the
# connection, and address is the address bound to the socket on the other
# end of the connection.
    conn, addr = server_socket.accept()
    print(f"Nueva conexion desde {addr}...")

    while conn:
        data = str(conn.recv(4096), "utf-8")
        
        if not data:
            break
        
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
