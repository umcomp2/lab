import multiprocessing as mp
import sys
import os

EOF = b''
RGB = ['r', 'g', 'b']

class Histogramer(mp.Process):
    def __init__(self, color, pipe, chunk_sz, file_name: str):
        super(Histogramer, self).__init__()
        self.color = color
        self.pipe = pipe
        self.chunk_sz = chunk_sz
        self.file_name = file_name.replace('.ppm', '')
        self.histogram = dict()

    # TODO: Se podria optimizar para que no haga falta rellenar
    #       el pixel completo y solo vaya saltando entre los
    #       bytes utiles. Pero es una buena primer aproximacion
    def run(self):
        mod_chunk = b'P6\n256 256\n255\n'
        fd = os.open(f'{RGB[self.color]}_{self.file_name}.ppm', os.O_RDWR | os.O_CREAT)
        
        # Puntero
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
            os.write(fd, mod_chunk)
            mod_chunk = b''
            if len(chunk) < self.chunk_sz and\
                EOF in chunk:
                break
        try:
            self.dump_histogram()
        except Exception as e:
            print(f'Error inesperado al escribir histograma {RGB[self.color]}. Error {e}')

        sys.exit(0)


    def add_entrada(self, depth):
        if depth in self.histogram:
            self.histogram[depth] += 1
        else:
            self.histogram[depth] = 1
        return

    def str_histogram(self):
        ord_keys = list(self.histogram.keys())
        string = f'\t{RGB[self.color]}\t\tFrecuencia absoluta\n'
        string += f'\t---\t\t---------------------\n'
        for i in sorted(ord_keys):
            string += f'\t{i}\t\t{self.histogram[i]}\n'
        return string

    def sum_histogram(self):
        s = 0
        for i in self.histogram:
            s += self.histogram[i]
        return s

    def dump_histogram(self):
        fd = os.open(f'{RGB[self.color]}_{self.file_name}.txt', os.O_RDWR | os.O_CREAT)
        os.write(fd, bytes(self.str_histogram(), 'utf-8'))
        return
