import argparse


class Parser:
    @staticmethod
    def parser():
        parser = argparse.ArgumentParser(description='Cliente-servidor')
        parser.add_argument('-i', '--ip', help='Ingrese host')
        parser.add_argument('-p', '--port', type=int, help='Ingrese puerto')
        args = parser.parse_args()
        return args