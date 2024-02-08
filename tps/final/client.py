
  
import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="ip", type=str)
parser.add_argument("-p", "--puerto", help="puerto", type=int)
parser.add_argument("-u", "--admin", help="Indica que el tipo de usuario", action="store_true", required=False)

argumento = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# sock.connect((argumento.ip, argumento.puerto))

# mensaje = ""
# if argumento.rol:
#     mensaje = "administrador"
# else:
#     mensaje = "usuario_comun"

mensaje = input("Ingrese un mensaje")

# Crear el socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectar al servidor
    sock.connect((argumento.ip, argumento.puerto))

    # Enviar el mensaje al servidor
    sock.sendall(mensaje.encode())

    # Esperar la respuesta del servidor
    data = sock.recv(1024)
    print("Respuesta del servidor:", data.decode())

    # Esperar la entrada del usuario antes de cerrar la conexión
    input("Presiona Enter para cerrar la conexión...")

except Exception as e:
    print("Error:", e)

finally:
    # Cerrar el socket
    print('Cerrando el socket')
    sock.close()