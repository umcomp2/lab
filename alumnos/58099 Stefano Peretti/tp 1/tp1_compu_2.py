#!/usr/bin/python3
# tp1_compu_2.py -f C:\Users\Stefano\yacht.ppm
import os
import array
import argparse
import concurrent.futures as fut

class Fromato_no_valido(Exception):
    def __init__(self, message):
        print(message)


class archivo_null(Exception):
    def __init__(self, message):
        print(message)

class Imagen():
    def __init__(self, path, nombre):

        self.path = path
        if not nombre:
            raise archivo_null("No ha detectado ningun archivo")

        if not nombre.endswith(".ppm"):
            raise Fromato_no_valido("Formato invalido")

        print('Realizando fotos...')
        
        with open(nombre, "rb") as archivo:
            self.imagen = archivo.read()
        
        conteo = 0
        contador = 0

        # IMG HEADER obtener y reemplazar

        for num in range(len(self.imagen)):
            contenido_posicion = self.imagen[num]

            if chr(contenido_posicion) == "\n":
                contador += 1
            elif chr(contenido_posicion) == "#":
                contador -= 1

            if contador == 3:
                conteo += 1
            if conteo == 2:
                self.header = self.imagen[:num]
                break

        self.body = self.imagen.replace(self.header, b"")
        self.header = self.header.decode()
        self.lista_imagen = [i for i in self.body]


class Color_canal():
    def __init__(self, color, lista_imagen, header, intensidad=1):

        print('Procesos ID: '+str(os.getpid()))
        self.header = header
        self.color_max = int(self.header.split()[-1])
        self.filterImage = [0 for i in lista_imagen]

        for i in range(color, len(lista_imagen), 3):
            self.filterImage[i] = lista_imagen[i]

        self.filtro_img = [int(i * intensidad)
                                  if i * intensidad <= self.color_max
                                  else self.color_max
                                  for i in self.filterImage]

    def intensidad(self, intensidad):
        self.filtro_img = [int(i * intensidad)
                                  if i * intensidad <= self.color_max
                                  else self.color_max
                                  for i in self.filterImage]

        return self.filtro_img

    def write(self, path, nombre):
        imagen = array.array('B', self.filtro_img)

        with open(path + nombre, "wb", os.O_CREAT) as x:
            x.write(bytearray(self.header, 'ascii'))
            imagen.tofile(x)

def aplicar_capas(path, nombre, header, *args):
   
    color_max = int(header.split()[-1])
    fusion = [sum(i) 
            if sum(i) <= color_max
            else color_max 
            for i in zip(*args)]
    # B = unsinged char
    imagen = array.array('B', fusion)

    with open(path + nombre, "wb", os.O_CREAT) as x:
        x.write(bytearray(header, 'ascii'))
        imagen.tofile(x)


def procesos_hijos(path, nombre, color, lista_imagen, header, intensidad):

    channel = Color_canal(color, lista_imagen, header, intensidad)
    channel.write(path, nombre)
    return channel.filtro_img

def metodo_a_ejecutar():

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--imgppm", help="Img ppm")
    parser.add_argument("-n", "--bloque", type=int, default=0,help="tamanio bloque")
    parser.add_argument("-r", "--red", type=int, default=1,help="Inserte red/rojo")
    parser.add_argument("-g", "--green", type=int, default=1,help="Inserte green/verde")
    parser.add_argument("-b", "--blue", type=int, default=1,help="Inserte blue/azul")

    args = parser.parse_args()
    path = __file__.replace("TP.py", "")
    nombre = args.imgppm

    i = Imagen(path, nombre)

    with fut.ProcessPoolExecutor() as colores:

        path = nombre
        print(path)
        r = colores.submit(procesos_hijos, path, "img_roja.ppm",0, i.lista_imagen, i.header, args.red)
        g = colores.submit(procesos_hijos, path, "img_verde.ppm",1, i.lista_imagen, i.header, args.green)
        b = colores.submit(procesos_hijos, path, "img_azul.ppm",2, i.lista_imagen, i.header, args.blue)
    aplicar_capas(path, "img_completa.ppm", i.header, r.result(), g.result(), b.result())
    print("Las imagennes han sido creadas exitosamente")

if __name__ == "__main__":
    metodo_a_ejecutar()