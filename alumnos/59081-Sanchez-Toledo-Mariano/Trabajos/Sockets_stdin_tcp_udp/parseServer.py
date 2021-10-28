from argparse import *
import argparse

class Parse:
    def parser():
        parser = argparse.ArgumentParser(description='Server tcp-udp')
        parser.add_argument('-p', '--port', type=int, help='Ingrese el puerto')
        parser.add_argument('-t', '--type', type=str, help='Ingrese modo tcp/udp')
        parser.add_argument('-f', '--file', type=str, help='Ingrese ruta a archivo')
        args = parser.parse_args()
        return args