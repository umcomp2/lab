import socket
import subprocess
import argparse


args = argparse.ArgumentParser()
args.add_argument("-hs", "--host", help="host", type=str)
args.add_argument("-p", "--port", help="port", type=int)
argument = args.parse_args()

sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST=argument.host
PORT=argument.port
sock_server.bind((HOST, PORT)) 
sock_server.listen(1)

while True:
    print('Waiting for client connection')
    connection, client_address = sock_server.accept()

    try:
        print('Connection from ', client_address)
        while True:
            data = connection.recv(1024)
            if not data:
                print('No data: ', client_address)
                break

            print('Received: ',data.decode('UTF-8'))
            data=data.split()
            command=subprocess.run(data, capture_output=True,shell=True)
            if command.returncode == 0:
                print('OK Data')
                stdout=str(command.stdout,'UTF-8')
                connection.sendall(bytes('OK\n'+stdout,'UTF-8'))
            else:
                stderr=str(command.stderr,'UTF-8')
                connection.sendall(bytes('ERROR\n'+stderr,'UTF-8'))

    finally:
        connection.close()