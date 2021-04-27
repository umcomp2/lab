#!/usr/bin/python3
import os
import argparse
import array
import time
from multiprocessing import Process, Pipe
import matplotlib.pyplot as plot


def prosRojo(pipe, nombre_archivo, imageInt, header):
    rojo = []
    rojo_unico = []
    # recorro los num dentro del rango de la cant de pixeles de imageInt
    for num in range(len(imageInt)):
        # me posiciono en el pixel rojo
        if num % 3 == 0 or num == 0:
            # profundidad del pixel
            r = int(imageInt[num])
            # acumulo los pixeles rojos en un array de enteros
            rojo += [r] + [0] + [0]
            rojo_unico += [r]
    # envio al pipe por el descriptor del hijo
    print(len(rojo_unico))
    pipe.send(rojo_unico)
    pipe.close()
    # creo un array de bytes que representa los pixeles de la imagen
    imagenRojo = array.array('B', [i for i in rojo])
    # creo la imagen roja
    with open("FiltroRojo_" + nombre_archivo, "wb", os.O_CREAT) as img:
        # le agrego el header
        img.write(header)
        # escribo el array de que representa la imagen roja en la img
        imagenRojo.tofile(img)
        img.close()


def prosVerde(pipe, nombre_archivo, imageInt, header):
    verde = []
    verde_unico = []
    for num in range(len(imageInt)):
        if (num-1) % 3 == 0 or num == 1:
            v = int(imageInt[num])
            verde += [0] + [v] + [0]
            verde_unico += [v]
    pipe.send(verde_unico)
    pipe.close()
    imagenVerde = array.array('B', [i for i in verde])
    with open("FiltroVerde_" + nombre_archivo, "wb", os.O_CREAT) as img:
        img.write(header)
        imagenVerde.tofile(img)
        img.close()


def prosAzul(pipe, nombre_archivo, imageInt, header):
    azul = []
    azul_unico = []
    for num in range(len(imageInt)):
        if (num-2) % 3 == 0 or num == 2:
            a = int(imageInt[num])
            azul += [0] + [0] + [a]
            azul_unico += [a]
    pipe.send(azul_unico)
    pipe.close()
    imagenAzul = array.array('B', [i for i in azul])
    with open("FiltroAzul_" + nombre_archivo, "wb", os.O_CREAT) as img:
        img.write(header)
        imagenAzul.tofile(img)
        img.close()


def parserImages():
    parser = argparse.ArgumentParser(description='Tp1 - procesa ppm')
    parser.add_argument(
        '-s', '--size', type=int, default=1024, help='Bloque_lectura')
    parser.add_argument('-f', '--file', help='Archivo a procesar')
    return parser.parse_args()


def abrir_y_leer_imagen(nombre_archivo):
    time.sleep(2)
    # Abro la imagen y la leo
    path = './'
    imagen = open(path + nombre_archivo, "rb").read()
    return imagen


def header_and_body(imagen):
    finHeader = imagen.find(
        b"\n", imagen.find(b"\n", imagen.find(b"\n") + 1) + 1) + 1
    # Guardo el header y el body
    header = imagen[:finHeader]
    body = imagen[finHeader:]
    # Pixeles a int
    imageInt = [i for i in body]
    print(len(imageInt))
    return header, imageInt


def eliminarComentarios(imagen):
    cantComentarios = imagen.count(b"\n# ")
    for num in range(cantComentarios):
        # posicion en la que se encuentra el {com1}
        com1 = imagen.find(b"\n# ")
        # posicion del segundo {com2} desde la pos sig a la pos de {com1}
        # donde termina el comentario
        com2 = imagen.find(b"\n", com1 + 1)
        # elimino el comentario
        imagen = imagen.replace(imagen[com1:com2], b"")
    return imagen


def crearHijos(pipeH1, pipeH2, pipeH3, nombre_archivo, imageInt, header):
    print("creando")
    hr = Process(
        target=prosRojo, args=(pipeH1, nombre_archivo, imageInt, header))
    hv = Process(
        target=prosVerde, args=(pipeH2, nombre_archivo, imageInt, header))
    ha = Process(
        target=prosAzul, args=(pipeH3, nombre_archivo, imageInt, header))
    print("arrancando")
    hr.start()
    hv.start()
    ha.start()
    hr.join()
    hv.join()
    ha.join()


def crearHistogramas(color, nombre_archivo, nombre):
    # divido en 8 intervalos
    intervalos = [0, 32, 64, 96, 128, 160, 192, 224, 256]
    plot.hist(x=color, bins=intervalos, color='#F2AB6D', rwidth=0.85)
    plot.title(f'Histograma de intensidad de color RGB de {nombre_archivo}')
    plot.xlabel('Escala de Color')
    plot.ylabel('Frecuencia')
    plot.xticks(intervalos)
    # dibujamos el histograma
    plot.savefig(nombre)


if __name__ == '__main__':
    try:
        args = parserImages()
        nombre_archivo = args.file
    except IOError:
        print("ERROR - Argumentos invalidos")
        exit()
    except NameError:
        print("\nDebe ingresar el nombre de la imagen.ppm\n")
        exit()
    try:
        print("El padre esta leyendo el archivo")
        imagen = abrir_y_leer_imagen(nombre_archivo)
        print("Imagen leida correctamente")
    except Exception:
        print("ERROR - Error al leer la imagen, verifique la direccion")
        exit()
    try:
        imagenSinCom = eliminarComentarios(imagen)
        print("comentarios eliminados correctamente")
        header, imageInt = header_and_body(imagenSinCom)
        print("header y body separados correctamente")
        time.sleep(2)
    except Exception:
        print("ERROR - Error en el header de la imagen")
        exit()
    try:
        print("creo los descriptores")
        pipePH1, pipeH1 = Pipe()
        pipePH2, pipeH2 = Pipe()
        pipePH3, pipeH3 = Pipe()
        print("Llamando hijos")
        crearHijos(pipeH1, pipeH2, pipeH3, nombre_archivo, imageInt, header)
        print("Colores procesados correctamente")
        print("recibiendo las listas de los hijos")
        pix_rojo = pipePH1.recv()
        pix_verde = pipePH2.recv()
        pix_azul = pipePH3.recv()
        pipePH1.close()
        pipePH2.close()
        pipePH3.close()
    except Exception:
        print("ERROR - No se pudieron procesar los colores")
        exit(2)
    try:
        crearHistogramas(pix_rojo, nombre_archivo, "histogramaRojo.png")
        crearHistogramas(pix_verde, nombre_archivo, "histogramaVerde.png")
        crearHistogramas(pix_azul, nombre_archivo, "histogramaAzul.png")
    except Exception:
        print("ERROR - No se pudo crear el histograma")
        exit(2)
