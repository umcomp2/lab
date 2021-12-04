import argparse
from os import truncate
import socket
import pickle
import cv2
from PIL import Image
import json
import base64
from io import BytesIO
import numpy as np

parserito = argparse.ArgumentParser(description="Procesamiento de imagenes")

parserito.add_argument("-i", "--ip", dest="ip", help="ip", type=str, required=True)
parserito.add_argument("-p", "--puerto", dest="puerto",
                       help="Puerto", type=int, required=True)
parserito.add_argument("-im", "--imagen", dest="imagen",
                       help="Imagen a la que le quiere aplicar los cambios", type=str, required=True)
parserito.add_argument("-e", "--edicio", dest="edicion",
                       help="Que edicion le quiere realizar a la imagen?", type=str, required=True)
parserito.add_argument("-n1", "--n1", dest="n1", help="numero 1", type=int)
parserito.add_argument("-n2", "--n2", dest="n2", help="numero 2", type=int)
parserito.add_argument("-n3", "--n3", dest="n3", help="numero 3", type=int)
parserito.add_argument("-n4", "--n4", dest="n4", help="numero 4", type=int)
parserito.add_argument("-t", "--texto", dest="texto", help="texto para agregar a la imagen")

args = parserito.parse_args()

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect((args.ip, args.puerto))

lista = [args.imagen, args.edicion, args.n1, args.n2, args.n3, args.n4, args.texto] 
msg = []
for i in lista:
    if i != None:
        msg.append(i)
serializador = pickle.dumps(msg)
socket.sendall(serializador) 

datos = str(socket.recv(500000), "utf-8")

img = json.dumps(datos)
img = base64.b64decode(img)
img = BytesIO(img)
img = Image.open(img)
img.show()
print(">>>>>>>>>> Servidor desconectado <<<<<<<<<<")
socket.close()

