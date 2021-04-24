import multiprocessing as mp
from multiprocessing import connection
import sys
import os

EOF = b''
RGB = ['r', 'g', 'b']

class Histogramer(mp.Process):
    def __init__(self, color: int, pipe: connection.Connection, chunk_sz: int, file_name: str, header: str):
        super(Histogramer, self).__init__()
        self.color = color
        self.pipe = pipe
        self.chunk_sz = chunk_sz
        self.file_name = file_name.replace('.ppm', '')
        self.header = header
        self.histogram = dict()

    def run(self):
        # Modified chunk que se utiliza en la creacion de los .ppm
        # con filtro e color respectivo al proceso que lo trato.
        # Inicia con la cabecera recibida por constructor
        mod_chunk = bytes(self.header, 'utf-8')

        # Crear archivo y abrirlo en modo read & write
        fd = os.open(f'{RGB[self.color]}_{self.file_name}.ppm', os.O_RDWR | os.O_CREAT)
        
        # Puntero que indica posicion de lectura actual
        cursor = 0

        while True:
            chunk = self.pipe.recv()

            for i in chunk:
                if cursor % 3 == self.color:
                    self.add_entrada(i)
                    mod_chunk += bytes([i])
                else:
                    mod_chunk += b'\x00'

                cursor += 1

            # Escribo al archivo ppm el chunk modificado y reinicio
            os.write(fd, mod_chunk)
            mod_chunk = b''

            # Compruebo si aun queda informacion en el pipe
            if len(chunk) < self.chunk_sz and\
                EOF in chunk:
                break

        # Manejo de error en caso de que algo inesperado pase al momento
        # de escribir al archivo el histograma
        try:
            self.dump_histogram()

        except Exception as e:
            print(f'Error inesperado al escribir histograma {RGB[self.color]}. Error {e}')

        # Tareas del hogar
        self.pipe.close()
        os.close(fd)
        
        sys.exit(0)

    # Aumenta en 1 la frec. abs. de la profundidad del color pasada
    # por parametros.
    #   @depth: Profundidad a la cual aumentar el contador
    def add_entrada(self, depth):
        if depth in self.histogram:
            self.histogram[depth] += 1
        else:
            self.histogram[depth] = 1
        return

    # Formatea el histograma(diccionario) que mantiene el objeto a texto
    # capaz de salir por STDOUT o ir a un archivo .txt
    def str_histogram(self):
        ord_keys = list(self.histogram.keys())
        string = f'\t{RGB[self.color]}\t\tFrecuencia absoluta\n'
        string += f'\t---\t\t---------------------\n'
        for i in sorted(ord_keys):
            string += f'\t{i}\t\t{self.histogram[i]}\n'
        return string

    # Funcion a modo de test para ver que se cuentan todos los pixeles
    def sum_histogram(self):
        s = 0
        for i in self.histogram:
            s += self.histogram[i]
        return s

    # Escribe a disco el histograma correspondiente al color que maneja
    # el proceso
    def dump_histogram(self):
        fd = os.open(f'{RGB[self.color]}_{self.file_name}.txt', os.O_RDWR | os.O_CREAT)
        os.write(fd, bytes(self.str_histogram(), 'utf-8'))
        os.close(fd)
        return
