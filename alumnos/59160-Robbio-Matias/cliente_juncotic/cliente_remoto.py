import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--host", action="store",default='127.0.0.1', type= str)
parser.add_argument("-p","--port", type=int,action="store",required=True)
args = parser.parse_args()

HOST = args.host
PORT = args.port

cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cliente.connect((HOST,PORT))

commands = ['hello|','email|','key|','exit']
errors = {
    "200":"OK",
    "400":"Comando válido, pero fuera de secuencia.",
    "500":"Comando inválido.",
    "404":"Clave errónea.",
    "405":"Cadena nula."
}

i = 0
while True:
    if i == 0:
        prompt = "Ingrese su nombre"
    if i == 1:
        prompt = "Ingrese su email"
    if i == 2:
        prompt = "Ingrese su clave"
    
    user_input = str(input(f"{prompt} : "))
    msg = commands[i]+user_input
    cliente.send(msg.encode('ascii'))
    ans = str(cliente.recv(512),'ascii')

    if ans == "200":
        i += 1
        print("OK")

    else:
        print(f"ERROR\n{errors[ans]}\nIntente de nuevo")
    
    if i == 3:
        print("Todos los pasos se ejecutaron correctamente")
        cliente.send(commands[3].encode('ascii'))
        cliente.close()
        break


