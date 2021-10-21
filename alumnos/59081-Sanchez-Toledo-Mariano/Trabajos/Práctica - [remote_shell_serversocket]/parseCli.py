import argparse

class Parser:
    def parser():
        parser = argparse.ArgumentParser(description='Cliente-servidor')
        parser.add_argument('-l', '--log', action='store_true', help='Indique la ruta del archivo')
        args = parser.parse_args()
        return args