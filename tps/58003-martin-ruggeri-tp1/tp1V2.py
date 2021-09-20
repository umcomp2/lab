#!/usr/bin/python3
import os
import argparse
import array
import time
from multiprocessing import Process, Queue
import matplotlib.pyplot as plot


def prosRojo(q1, nombre_archivo, imageInt, header, imgGrande):
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
    if imgGrande:
        comprimido = {}
        for i in range(256):
            comprimido[i] = rojo_unico.count(i)
        q1.put(comprimido)
    else:
        q1.put(rojo_unico)
    # creo un array de bytes que representa los pixeles de la imagen
    imagenRojo = array.array('B', [i for i in rojo])
    # creo la imagen roja
    with open("FiltroRojo_" + nombre_archivo, "wb", os.O_CREAT) as img:
        # le agrego el header
        img.write(header)
        # escribo el array de que representa la imagen roja en la img
        imagenRojo.tofile(img)
        img.close()


def prosVerde(q2, nombre_archivo, imageInt, header, imgGrande):
    verde = []
    verde_unico = []
    for num in range(len(imageInt)):
        if (num-1) % 3 == 0 or num == 1:
            v = int(imageInt[num])
            verde += [0] + [v] + [0]
            verde_unico += [v]
    if imgGrande:
        comprimido = {}
        for i in range(256):
            comprimido[i] = verde_unico.count(i)
        q2.put(comprimido)
    else:
        q2.put(verde_unico)
    imagenVerde = array.array('B', [i for i in verde])
    with open("FiltroVerde_" + nombre_archivo, "wb", os.O_CREAT) as img:
        img.write(header)
        imagenVerde.tofile(img)
        img.close()


def prosAzul(q3, nombre_archivo, imageInt, header, imgGrande):
    azul = []
    azul_unico = []
    for num in range(len(imageInt)):
        if (num-2) % 3 == 0 or num == 2:
            a = int(imageInt[num])
            azul += [0] + [0] + [a]
            azul_unico += [a]
    if imgGrande:
        comprimido = {}
        for i in range(256):
            comprimido[i] = azul_unico.count(i)
        q3.put(comprimido)
    else:
        q3.put(azul_unico)
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


def crearHijos(q1, q2, q3, nombre_archivo, imageInt, header, imgGrande):
    print("creando")
    hr = Process(
        target=prosRojo, args=(
            q1, nombre_archivo, imageInt, header, imgGrande))
    hv = Process(
        target=prosVerde, args=(
            q2, nombre_archivo, imageInt, header, imgGrande))
    ha = Process(
        target=prosAzul, args=(
            q3, nombre_archivo, imageInt, header, imgGrande))
    print("arrancando")
    hr.start()
    hv.start()
    ha.start()
    hr.join()
    hv.join()
    ha.join()


def crearHistogramas(color, nombre_archivo, nombre, imgGrande):
    if imgGrande:
        listaColor = []
        for i in color:
            for j in range(color[i]):
                listaColor.append(color[i])
        color = listaColor
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
    except Exception:
        print("ERROR - Error en el header de la imagen")
        exit()
    try:
        print("creo los descriptores")
        imgGrande = False
        q1 = Queue()
        q2 = Queue()
        q3 = Queue()
        if len(imageInt) > 200000:
            imgGrande = True
        print("Llamando hijos")
        crearHijos(q1, q2, q3, nombre_archivo, imageInt, header, imgGrande)
        print("Colores procesados correctamente")
        print("recibiendo las listas de los hijos")
        pix_rojo = q1.get()
        pix_verde = q2.get()
        pix_azul = q3.get()
    except Exception:
        print("ERROR - No se pudieron procesar los colores")
        exit(2)
    try:
        crearHistogramas(
            pix_rojo, nombre_archivo, "histogramaRojo.png", imgGrande)
        time.sleep(3)
        crearHistogramas(
            pix_verde, nombre_archivo, "histogramaVerde.png", imgGrande)
        time.sleep(3)
        crearHistogramas(
            pix_azul, nombre_archivo, "histogramaAzul.png", imgGrande)
    except Exception:
        print("ERROR - No se pudo crear el histograma")
        exit(2)
