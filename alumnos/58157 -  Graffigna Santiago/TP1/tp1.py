import argparse
import time
import os
from multiprocessing import Process, Queue
from collections import Counter
import cred

class Imagen():
    def __init__(self, path, name, bloque=0):
        
        # si no ingreso una imagen salta este error
        if not name:
            raise FileNotFoundError("No se pudo encontrar el archivo")

        # si el bloque es menor que cero salta este error
        if bloque < 0:
            raise ValueError("El valos del argumento size debe ser positivo")

        # si la imagen no es de formato .ppm salta este error
        if not name.endswith(".ppm"):
            raise TypeError("La imagen debe ser de tipo ppm")

        self.path = path

        self.size = os.path.getsize(path + name)
        
        # leo la imagen
        with open(self.path + name, "rb") as archivo:
            if bloque == 0:
                self.image = archivo.read()
            else:
                self.image = b""
                for num in range(round(self.size/bloque + 0.5)):
                    self.image += archivo.read(bloque)

        # busco el header para poder separarlo despues
        contador = 0
        espacios_en_blanco = 0
        for num in range(len(self.image)):
            item = self.image[num]

            if chr(item) == "\n":
                espacios_en_blanco += 1
            elif chr(item) == "#":
                espacios_en_blanco -= 1

            if espacios_en_blanco == 3:
                contador += 1
            if contador == 2:
                self.header = self.image[:num]
                break

        # aca separo el header
        self.body = self.image.replace(self.header, b"")
        self.header = self.header.decode()

        # lista con los pixels de la imagen
        self.imageList = [i for i in self.body]
        
# retorna un diccionario con el color pedido y todos los demas valores 0
def dicc(lista, rgb):
        desordenado = Counter(lista)    # diccionario con todos los colores desordenado
        ordenado = ordenador(desordenado)   # ordeno
        aux = {}
        
        if rgb == 'R':
            for key, value in ordenado.items():     # descarto los valores que no corresponden al color segun la posicion del color
                #if rgb == 'R':
                    if key % 3 == 0:
                        #print(key, value)
                        aux[key] = value
        
        if rgb == 'G':
            for key, value in ordenado.items():     # descarto los valores que no corresponden al color segun la posicion del color
                if key in cred.g_lista:
                    aux[key] = value

        if rgb == 'B':
            for key, value in ordenado.items():     # descarto los valores que no corresponden al color segun la posicion del color
                if key in cred.b_lista:
                    aux[key] = value
        
        for key in range(256):                      # los valores que no corresponden al color se ponen en 0
            if key not in aux:
                aux[key] = 0
        #print('aux')
        #print(ordenador(aux))
        # lo retorno ordenado
        return ordenador(aux)

# ordena el dicc
def ordenador(dicc):
    desordenado = dicc
    ordenado = {}
    for i in sorted(desordenado):
        ordenado[i] = desordenado[i]

    return ordenado

# escribe los diccionarios al archivo correspondiente
def escribir_archivo(dicc, rgb):
    #rgb = ['R', 'G', 'B']
    if rgb == 'R':
        with open('rojo.txt', 'w') as f:
            for key, value in dicc.items():
                f.write(f"{key}\t{value}\n")

    if rgb == 'G':
        with open('verde.txt', 'w') as f:
            for key, value in dicc.items():
                f.write(f"{key}\t{value}\n")

    if rgb == 'B':
        with open('azul.txt', 'w') as f:
            for key, value in dicc.items():
                f.write(f"{key}\t{value}\n")


# esto al final no lo uso asi que deberia de borrarlo
#def histograma(abc):
#    for key, value in abc.items():
#        print(key, value)


def main():

    # argumentos
    parser = argparse.ArgumentParser(description='TP1 Computacion II - Histograma con imagen ppm')

    parser.add_argument("-f", "--file", required=True, help="Nombre del archivo a seleccionar")
    parser.add_argument("-s", "--size", type=int, default=0, help="Size del bloque de bytes")

    args = parser.parse_args()
    path = __file__.replace("tp1.py", "")
    f = args.file
    s = args.size

    # instancio la clase Imagen con la que le paso por el argparse
    pic = Imagen(path, f, s)

    # obtengo la lista de los elementos de la clase Imagen
    listilla = pic.imageList

    # lo que va a terminar siendo el histograma
    abc_r = dicc(listilla, 'G')
    abc_g = dicc(listilla, 'G')
    abc_b = dicc(listilla, 'G')
    #dicc(listilla)
    #print('ROJO')
    #histograma(abc)

    #escribir_archivo(abc, 'G')
    # creo los procesos para escrbir los archivos
    process_r = Process(target=escribir_archivo, args=(abc_r, 'R'))
    process_g = Process(target=escribir_archivo, args=(abc_g, 'G'))
    process_b = Process(target=escribir_archivo, args=(abc_b, 'B'))

    # los arranco
    process_r.start()
    process_g.start()
    process_b.start()

    # los termino
    process_r.join()
    process_g.join()
    process_b.join()

    time.sleep(1)
    print('Terminado')
    #queue = Queue()


if __name__ == "__main__":
    main()