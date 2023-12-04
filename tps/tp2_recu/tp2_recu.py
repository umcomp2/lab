import argparse
import threading as th
import exceptions

# import time
barrier = th.Barrier(3)




def leer_archivo(archivo, size):
    
    # ABRIR ARCHIVO
    try:
        ppm = open(archivo, 'rb')
        # LEER EL ENCABEZADO
        header = []
        if archivo.endswith('.ppm'):
            # El strip()método elimina los caracteres iniciales (espacios al principio) y finales (espacios al final)/
            # (el espacio es el carácter inicial predeterminado para eliminar)
            num_magico = ppm.readline().strip()
            if num_magico == b"P6" or num_magico == b"P3":
                header.append(num_magico)
            else:
                raise exceptions.NoPPMfile

            # Hago un while para evitar que en el encabezado me muestre el "#"
            while True:
                ancho_alto = ppm.readline().strip()
                if ancho_alto.startswith(b"#"):
                    continue
                header.append(ancho_alto)
                break

            val_max = ppm.readline().strip()
            if val_max <= b"255":
                header.append(val_max)
            else:
                print("no puede pasar los 255")
            # print(header)
        else:
            raise exceptions.NoPPMfile
        # leer raster
        lista_roja = []
        lista_verde = []
        lista_azul = []
        while True:
            raster = ppm.read(size)
            if len(raster) == 0:
                break
            for i in range(0, len(raster)-1, 3):
                pix = raster[i:i+3]
                lista_roja.append(pix[0])
                lista_verde.append(pix[1])
                lista_azul.append(pix[2])
    
    except FileNotFoundError:
        print("El archivo no existe")
        exit()
    except exceptions.NoPPMfile:
        print("No es un archivo ppm")
        exit()
    return num_magico, ancho_alto, val_max, raster, lista_roja, lista_verde, lista_azul


def archivo_nuevo(archivo, size):
    num_magico, ancho_alto, val_max, raster, lista_roja, lista_verde, lista_azul = leer_archivo(
        archivo, size)
    header = (num_magico, ancho_alto, val_max)
    archivo_n = open("espejado_" + archivo, "wb")
    for i in header:
        archivo_n.write(i+b"\n")

def separar_ancho_alto(archivo, size):
    global matriz
    num_magico, ancho_alto, val_max, raster, lista_roja, lista_verde, lista_azul = leer_archivo(
        archivo, size)
    ancho = ancho_alto.split()[0]
    alto = ancho_alto.split()[1]
    matriz = [[["R","V","A"] for x in range(int(ancho))]for y in range(int(alto))]
    

    return ancho, alto




def hilo_rojo(archivo, size):
    global matriz
    num_magico, ancho_alto, val_max, raster, lista_roja, lista_verde, lista_azul = leer_archivo(
        archivo, size)
    ancho, alto = separar_ancho_alto(archivo, size)
    r = []
    for i in range(0, len(lista_roja), int(ancho)):
        pix_rojo = lista_roja[i:i+int(ancho)]
        r.append(pix_rojo)
    for i in r:
        i.reverse()

    for i in range(int(alto)):
        for j in range(int(ancho)):
            barrier.wait()
            matriz[i][j][0] = r[i][j]




def hilo_verde(archivo, size):
    global matriz
    num_magico, ancho_alto, val_max, raster, lista_roja, lista_verde, lista_azul = leer_archivo(
        archivo, size)
    ancho, alto = separar_ancho_alto(archivo, size)
    v = []
    for i in range(0, len(lista_verde), int(ancho) ):
        pix_verde = lista_verde[i:i+int(ancho)]
        v.append(pix_verde)

    for i in v:
        i.reverse()

    for i in range(int(alto)):
        for j in range(int(ancho)):
            barrier.wait()
            matriz[i][j][1] = v[i][j]




def hilo_azul(archivo, size):
    global matriz
    num_magico, ancho_alto, val_max, raster, lista_roja, lista_verde, lista_azul = leer_archivo(
        archivo, size)
    ancho, alto = separar_ancho_alto(archivo, size)
    
    b = []
    for i in range(0, len(lista_azul), int(ancho)):
        pix_azul = lista_azul[i:i+int(ancho)]
        b.append(pix_azul)
    for i in b:
        i.reverse()

    for i in range(int(alto)):
        for j in range(int(ancho)):
            barrier.wait()
            matriz[i][j][2] = b[i][j]



def imagen_espejada(archivo, size):
    global matriz
    archivo_nuevo(archivo, size)
    archivo_n = open("espejado_" + arg.archivo, "ab")
    
    for i in matriz:
        for j in i:
            archivo_n.write(bytes(j))


if __name__ == "__main__":

    # ARGUMENTOS
    parser = argparse.ArgumentParser(description="TPN°2/RECUPERATORIO")
    parser.add_argument('-f', '--file', required=True,
                        help="imagen a procesar", dest="archivo",)
    parser.add_argument('-s', '--size', default=1, type=int,
                        required=True, help='bloque de lectura', dest="size", )
    arg = parser.parse_args()

       # Size no negativo
    try:
        if arg.size < 0:
            raise exceptions.SizeNoNegativo
    except exceptions.SizeNoNegativo:
        print("Size no puede ser negativo")
        exit()

    # CREACION DE LOS HIJOS
    lista_hilos = []

    h_rojo = th.Thread(target=hilo_rojo, args=(arg.archivo, arg.size,))
    h_verde = th.Thread(target=hilo_verde, args=(arg.archivo, arg.size,))
    h_azul = th.Thread(target=hilo_azul, args=(arg.archivo, arg.size,))
    lista_hilos.append(h_rojo)
    lista_hilos.append(h_verde)
    lista_hilos.append(h_azul)

    # iniciar hilos
    for i in lista_hilos:
        i.start()
    # esperar hilos
    for i in lista_hilos:
        i.join()

    imagen_espejada(arg.archivo, arg.size)

    
