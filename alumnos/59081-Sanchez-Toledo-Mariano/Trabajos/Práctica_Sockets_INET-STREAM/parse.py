import argparse

class Parser:
    def parser():
        parser = argparse.ArgumentParser(description='Cliente-servidor')
        parser.add_argument('-l', '--log', help='Indique la ruta del archivo')
        args = parser.parse_args()
        return args