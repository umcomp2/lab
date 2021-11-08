import socket
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--server',action="store",default='127.0.0.1', type= str)
parser.add_argument('-p', '--port',action="store", type= int, required=True)
parser.add_argument('-f', '--file',action="store", required=True, type=str)
args = parser.parse_args()


SERVER = args.server
PORT = args.port
LOG = open(args.file,"w")

cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cliente.connect((SERVER,PORT))

while True:
    cmd = input("~$:")
    msg = cmd.encode('utf-8')
    cliente.send(msg)
    if cmd == '!DISCONNECT':
        break
    respuesta_server = str(cliente.recv(20000), "utf-8")
    print(respuesta_server)
    fecha = datetime.now()
    log_msg = str(f"{fecha}'\n'{cmd}'\n{respuesta_server}")
    LOG.write(log_msg)

cliente.close()
LOG.close