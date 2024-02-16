import argparse
import socket
import threading


def handleClient(client_socket):
    client_address = client_socket.getpeername()
    client_socket.send(b"Horarios disponibles: 9:00, 10:00, 16:00, 19:00\n")
    selected_time = client_socket.recv(1024).decode().strip()
    # Aquí iría la lógica para manejar la reserva del turno
    # Por ahora, solo confirmaremos la reserva y enviaremos un mensaje al cliente
    message = f"Reserva confirmada para {selected_time} el {client_address}"
    client_socket.send(message.encode())
    client_socket.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[INFO] Servidor escuchando en {host}:{port}...")

    while True:
        client_socket, _ = server.accept()
        print(f"[INFO] Conexión establecida desde {client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}")
        client_handler = threading.Thread(target=handleClient, args=(client_socket,))
        client_handler.start()





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #declaro los args para la conexion
    parser.add_argument("-i", "--ip", help="ip", type=str)
    parser.add_argument("-p", "--port", help="port", type=int)
    args = parser.parse_args()
    start_server(args.ip, args.port)

   