import socket
import argparse
import os

IP = socket.gethostname() 
EOF = b''


def createFile(fd):
    newFile =os.open(f'{fd}.txt', os.O_RDWR | os.O_CREAT)
    return newFile


def parser():
    parser = argparse.ArgumentParser(description='Connection to juncotic')
    parser.add_argument('-p', '--port', action="store", metavar='PORT', type=int,
                    required=True, help='Port of connection')
    parser.add_argument('-t', '--t', action="store", metavar='TRANSPORT', type=str,
                    required=True, help='Transport Protocol')
    parser.add_argument('-f', '--file', action="store", metavar='FILE', type=str,
                    required=True, help='File path')

    args = parser.parse_args()
    return args

def connect_to_client(conn, address):
    print(f'CONNECTION to host {address} SUCCESFUL')
    
    while True:
        message = ''
        data = conn.recv(4096)

        if data == b'exit':
            conn.close
            sys.exit(0)

        if not data: 
            break

        message += str(data, FORMAT)
        out = subprocess.run(message.split(), capture_output=True)
        exit = bool(out.returncode)

        if exit == False:
            conn.send(bytes((out.stdout.decode(FORMAT)),FORMAT))
        else:
            conn.send(out.stderr)

def create_soscket(protocol, ip, port):
    if protocol == 'tcp':
        
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((ip, port))
    
    if protocol == 'udp':
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind((ip, port))



def server_socket(protocol, port, ip, file):

    if protocol == 'tcp':
        
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind((ip, port))
        serverSocket.listen(5)

        conn, addr = serverSocket.accept()

        while True:
            chunk = conn.recv(4096)
            if chunk == EOF and len(chunk) < 4096:
                break
            os.write(file, chunk)


        
        










