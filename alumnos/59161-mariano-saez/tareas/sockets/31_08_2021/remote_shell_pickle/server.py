import socket
import sys
import subprocess
import signal
import concurrent.futures as cf
import pickle


def handler(signum, frame):
    print("\rCerrando server...")
    server_socket.close()
    exit(0)

# Para el cierre del server
signal.signal(signal.SIGINT, handler)


def recv_conn(conn, addr):
    while conn:
        serial_cmd = conn.recv(4096)
        data = pickle.loads(serial_cmd)
        
        if data == "bye":
            break
        
        command = data.split()
        returned = subprocess.run(command, capture_output=True)

        exit_code = bool(returned.returncode)

        if not exit_code:
            exit_stdout = str(returned.stdout, "utf-8")
            respuesta = pickle.dumps(f"OK\n{exit_stdout}")
        else:
            exit_stderr = str(returned.stderr, "utf-8")
            respuesta = pickle.dumps(f"ERROR\n{exit_stderr}")


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
print(f"Iniciando servidor en {HOST}:{PORT}...")
server_socket.bind((HOST, PORT))
# socket.listen([backlog])
# El backlog es la cantidad de conexiones que puede tener en espera
# para hacer el SYN-SYN/ACK-ACK
server_socket.listen()


while True:
# socket.accept()
# Accept a connection. The socket must be bound to an address
# and listening for connections. The return value is a pair (conn, address)
# where conn is a new socket object usable to send and receive data on the
# connection, and address is the address bound to the socket on the other
# end of the connection.
    conn, addr = server_socket.accept()
    print(f"Nueva conexion desde {addr}...")
    pool.submit(recv_conn, conn, addr)




    
