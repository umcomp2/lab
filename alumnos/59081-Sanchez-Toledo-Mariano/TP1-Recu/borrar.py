#!/usr/bin/python3
import os
import argparse
import array
import time
import multiprocessing

class prosColores():
    def __init__(self):
        self.rojo = []
        self.verde = []
        self.azul = []

    def prosRojo(self):
        for num in range(len(imageInt)):
            if num % 3 == 0 or num == 0:
                #Aumento el color con la escala seleccionada
                r = int(imageInt[num] * args.red)
                #Verifico que no supere los 255 bytes 
                if r > 255:
                    r = 255

                self.rojo += [r] + [0] + [0]

    def prosVerde(self):
        for num in range(len(imageInt)):
            if (num-1) % 3 == 0 or num == 1:
                v = int(imageInt[num] * args.green)
                if v > 255:
                    v = 255
                    
                self.verde += [0] + [v] + [0]

    def prosAzul(self):
        for num in range(len(imageInt)):
            if (num-2) % 3 == 0 or num == 2:
                a = int(imageInt[num] * args.blue)
                if a > 255:
                    a = 255

                self.azul += [0] + [0] + [a]

try:
    # Argumentos
    parser = argparse.ArgumentParser(description='Tp1 - procesa ppm')
    parser.add_argument('-r', '--red', type=float, default=0, help='Escala para rojo')
    parser.add_argument('-g', '--green', type=float, default=0, help='Escala para verde')
    parser.add_argument('-b', '--blue', type=float, default=0, help='Escala para azul')
    parser.add_argument('-s', '--size', type=int, help='Bloque de lectura')
    parser.add_argument('-f', '--file', help='Archivo a procesar')

    args = parser.parse_args()

except:
    print("ERROR - Argumentos invalidos")
    exit(2)

try:
    print("El padre", os.getpid(), "esta leyendo el archivo")
    time.sleep(2)

    #Abro la imagen y la leo
    imagen = open(args.file, "rb").read()

    #Fuera comentarios
    for num in range(imagen.count(b"\n# ")):
        com1 = imagen.find(b"\n# ")
        com2 = imagen.find(b"\n", com1 + 1)
        imagen = imagen.replace(imagen[com1:com2], b"")

    finHeader = imagen.find(b"\n", imagen.find(b"\n", imagen.find(b"\n") + 1) + 1) + 1

    #Guardo el header y el body
    header = imagen[:finHeader].decode()
    body = imagen[finHeader:]

    #Pixeles a int
    imageInt = [i for i in body]

    print("Imagen leida correctamente")
except:
    print("ERROR - Error al leer la imagen, verifique la direccion")
    exit(2)

time.sleep(3)

try:
    print("Llamando hijos")

    obj = prosColores()
    hr = multiprocessing.Process(target=obj.prosRojo(),  args=())
    hv = multiprocessing.Process(target=obj.prosVerde(),  args=())
    ha = multiprocessing.Process(target=obj.prosAzul(),  args=())

    hr.start()
    hv.start()
    ha.start()

    hr.join()
    hv.join()
    ha.join()

    print("Colores procesados correctamente")

except:
    print("ERROR - No se pudieron procesar los colores")
    exit(2)

time.sleep(2)

try:
    #Creo un array de las listas con los filtros hechos
    imagenRojo = array.array('B', [i for i in obj.rojo])
    imagenVerde = array.array('B', [i for i in obj.verde])
    imagenAzul = array.array('B', [i for i in obj.azul])

    #Creo las imagenes correspondientes
    with open("FiltroRojo_" + args.file, "wb", os.O_CREAT) as x:
        x.write(bytearray(header, 'ascii'))
        imagenRojo.tofile(x)
        x.close()

    with open("FiltroVerde_" + args.file, "wb", os.O_CREAT) as x:
        x.write(bytearray(header, 'ascii'))
        imagenVerde.tofile(x)
        x.close()

    with open("FiltroAzul_" + args.file, "wb", os.O_CREAT) as x:
        x.write(bytearray(header, 'ascii'))
        imagenAzul.tofile(x)
        x.close()

    print("Imagen creada correctamente")

except:
    print("ERROR - La imagen no pudo ser creada")
    exit(2)