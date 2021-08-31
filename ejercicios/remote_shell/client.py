import socket
import argparse


args = argparse.ArgumentParser()
args.add_argument("-hs", "--host", help="host", type=str)
args.add_argument("-p", "--port", help="port", type=int)
argument = args.parse_args()

sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST=argument.host
PORT=argument.port
serverAddress=((HOST,PORT))
sock_client.connect(serverAddress)

while True:
    message = input('##: ')
    sock_client.sendall(bytes(message,encoding='UTF-8'))
    data = sock_client.recv(1024)
    print(data.decode('UTF-8'))

    if message == 'exit':
        break
print('Closing')
sock_client.close()