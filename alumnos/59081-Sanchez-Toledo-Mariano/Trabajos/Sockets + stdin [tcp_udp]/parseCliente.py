import argparse

class Parse:
    def parser():
        parser = argparse.ArgumentParser(description='Server tcp-udp')
        parser.add_argument('-a', type=str, help='ingrese ip del servidor')
        parser.add_argument('-p', '--port', type=int, help='Ingrese el puerto')
        parser.add_argument('-t', '--type', type=str, help='Ingrese modo tcp/udp')
        args = parser.parse_args()
        return args