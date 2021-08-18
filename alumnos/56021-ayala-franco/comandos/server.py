import socket
import concurrent.futures
import subprocess

def execute(client_socket: socket.socket):
    client_socket.settimeout(100.0)
    while True:
        try:
            command = client_socket.recv(100)
            result = subprocess.run(command, capture_output=True, encoding="UTF-8")
        except socket.timeout:
            break
        response = f"=== Execution Result: {str(result.returncode)} ===\n{result.stdout}=== Execution End ==="
        client_socket.send(bytes(response, "UTF-8"))
    client_socket.shutdown(socket.SHUT_RDWR)

process_pool = concurrent.futures.ProcessPoolExecutor(5)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 51007))
server_socket.listen(5)
while True:
    client_socket, addr = server_socket.accept()
    process_pool.submit(execute, client_socket)