import socket
import subprocess
import argparse
import threading

args = argparse.ArgumentParser()
args.add_argument("-hs", "--host", help="host", type=str)
args.add_argument("-p", "--port", help="port", type=int)
argument = args.parse_args()

def thread_server(clientsocket,addr):
    try:
        print('Connection from ', addr)
        while True:
            data = clientsocket.recv(1024)
            if not data:
                print('No data: ', addr)
                break

            print('Received: ',data.decode('UTF-8'))
            data=data.split()
            command=subprocess.run(data, capture_output=True,shell=True)
            if command.returncode == 0:
                print('OK Data')
                stdout=str(command.stdout,'UTF-8')
                clientsocket.sendall(bytes('OK\n'+stdout,'UTF-8'))
            else:
                stderr=str(command.stderr,'UTF-8')
                clientsocket.sendall(bytes('ERROR\n'+stderr,'UTF-8'))

    finally:
        clientsocket.close()

sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST=argument.host
PORT=argument.port
sock_server.bind((HOST, PORT)) 
sock_server.listen(1)

while True:
    print('Waiting for client connection')
    connection, client_address = sock_server.accept()
    th=threading.Thread(target=thread_server, args=(connection, client_address,))
    th.start()