import socket, sys

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Falied to create socket")
    sys.exit()

# python client_dgra.py ip_server puerto_server

host = sys.argv[1]
port = int(sys.argv[2])

while(1):
    msg = input("Enter message to send: ").encode()
    try:
        # set the whole string
        s.sendto(msg, (host, port))
        # recive data from client ( data, addr)
        # quedo esperando la data
        d = s.recvfrom(1024)
        # dato de respuesta
        reply = d[0]
        # tupla host port de la respuesta
        addr = d[1]
        print("Server reply: " + reply.decode())
    except socket.error:
        print(" Error code: " + str(msg[0] + "menssage " + msg[1]))