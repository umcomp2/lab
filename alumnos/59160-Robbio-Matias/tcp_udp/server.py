import socket
import argparse

def start_server(protocol,port):
    if protocol == 'tcp':
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    
    elif protocol == 'udp':
        server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    server.bind(('0.0.0.0',port))
    print(f"Servidor inizializado")
    return server

def tcp_handler(server,file):
    server.listen()
    conn, addr = server.accept()
    print(f"Nueva conexion establecida[cliente:{addr}]")
    while True:
        read = conn.recv(4096)
        file.write(read.decode('utf-8'))
        if read.decode() == "":
            print(f"Finalizando conexion con {addr}")
            conn.close()
            break
        conn.send(b"Recibido")
        

def udp_handler(server,file):
    while True:
        read,addr = server.recvfrom(4096)
        file.write(read.decode('utf-8'))
        if read.decode() == "":
            print(f"Conexion finalizada por {addr}")
            break



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file',action="store", type= str,required=True)
    parser.add_argument('-p', '--port',action="store", type= int, required=True)
    parser.add_argument('-t', '--tprotocol',action="store",choices=['tcp','udp'], required=True, type=str)
    args = parser.parse_args()

    FILE = open(args.file,"w")
    PORT = args.port
    PROTOCOL = args.tprotocol

    SERVER = start_server(PROTOCOL,PORT)
    
    if PROTOCOL == 'tcp':
        tcp_handler(SERVER,FILE)
    if PROTOCOL == 'udp':
        udp_handler(SERVER,FILE)
    
    FILE.close()
    print("Cerrando Server")
    SERVER.close()

