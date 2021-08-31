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

form = ['hello|','email|','key|','out|']
for element in form:
    error = True
    while error == True:
        value = input(element)
        result = element + value
        if element == 'out|':
            result = value
        sock_client.sendall(bytes(result,encoding='UTF-8'))
        data = sock_client.recv(1024)
        print(data.decode('UTF-8'))
        if data.decode('UTF-8') == '200':
            error = False
            
print('Closing')
sock_client.close()