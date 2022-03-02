import argparse
import socket
import pickle
from PIL import Image
import json
import base64
from io import BytesIO
import os
import shutil
import configparser

parserito = argparse.ArgumentParser(description="Procesamiento de imagenes")


parserito.add_argument("-ar", "--archivo", dest="archivo",
                       help="archivo ini con configuraciones", type=str)
parserito.add_argument("-i", "--ip", dest="ip",
                       help="ip", type=str)
parserito.add_argument("-p", "--puerto", dest="puerto",
                       help="Puerto", type=int)
parserito.add_argument("-n", "--nombre", dest="nombre",
                       help="nombre de la persona que realiza la edicion", type=str)
parserito.add_argument("-d", "--directorio", dest="directorio",
                       help="en donde quiere guardar la imagen?", type=str)
parserito.add_argument("-im", "--imagen", dest="imagen",
                       help="Imagen a la que le quiere aplicar los cambios", type=str)
parserito.add_argument("-e", "--edicio", dest="edicion",
                       help="Que edicion le quiere realizar a la imagen?", type=str)
parserito.add_argument("-n1", "--n1", dest="n1", help="numero 1", type=int)
parserito.add_argument("-n2", "--n2", dest="n2", help="numero 2", type=int)
parserito.add_argument("-n3", "--n3", dest="n3", help="numero 3", type=int)
parserito.add_argument("-n4", "--n4", dest="n4", help="numero 4", type=int)
parserito.add_argument("-t", "--texto", dest="texto",
                       help="texto para agregar a la imagen")

args = parserito.parse_args()

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if args.archivo:
    config = configparser.ConfigParser()
    config.read(args.archivo)
    # config.sections() ['conexion', 'datos_personales', 'datos_imagen', 'parametros_imagen']
    args.puerto = int(config["conexion"]["port"])
    args.ip = config["conexion"]["ip"]
    args.nombre = config["datos_personales"]["nombre"]
    args.directorio = config["datos_personales"]["directorio"]
    args.imagen = config["datos_imagen"]["imagen"]
    args.edicion = config["datos_imagen"]["edicion"]
    if config["parametros_imagen"]["n1"] != "":
        args.n1 = int(config["parametros_imagen"]["n1"])
    else:
        args.n1 = config["parametros_imagen"]["n1"]
    if config["parametros_imagen"]["n2"] != "":
        args.n2 = int(config["parametros_imagen"]["n2"])
    else:
        args.n2 = config["parametros_imagen"]["n2"]
    if config["parametros_imagen"]["n3"] != "":
        args.n3 = int(config["parametros_imagen"]["n3"])
    else:
        args.n3 = config["parametros_imagen"]["n3"]
    if config["parametros_imagen"]["n4"] != "":
        args.n4 = int(config["parametros_imagen"]["n4"])
    else:
        args.n4 = config["parametros_imagen"]["n4"]
    args.texto = config["parametros_imagen"]["texto"]

socket.connect((args.ip, args.puerto))

lista = [args.imagen, args.edicion, args.n1, args.n2,
         args.n3, args.n4, args.texto, args.nombre]
msg = []
for i in lista:
    if i != None:
        msg.append(i)
serializador = pickle.dumps(msg)
socket.sendall(serializador)

with open("inf.txt", "w+") as archivo1:
    while True:
        datos = str(socket.recv(4096), "utf-8")
        archivo1.write(datos)
        if len(datos) != 4096:
            break
    archivo1.close()

with open("inf.txt", "r+") as archivo:
    raster = archivo.read()
    img = json.dumps(raster)
    img = base64.b64decode(img)
    img = BytesIO(img)
    img = Image.open(img)
    img.save(args.edicion+"_"+args.imagen)
archivo.close()
os.remove(os.getcwd()+"/inf.txt")
os.makedirs(args.directorio, exist_ok=True)
shutil.move(args.edicion+"_"+args.imagen, args.directorio)


print(">>>>>>>>>> Servidor desconectado <<<<<<<<<<")
socket.close()
