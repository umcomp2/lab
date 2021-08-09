import argparse

class Parser():
    def parser():
        parser = argparse.ArgumentParser(description='Rotador de imagenes ppm!!')
        parser.add_argument('-f', '--file', type=str,
                            help='Indique la ruta del archivo')
        #parser.add_argument('-s', '--size', type=int,
        #                    help='Indique tamaño de bloque de lectura')
        args = parser.parse_args()

        return args
