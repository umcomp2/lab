import argparse

class Parser:
    def parser():
        parser = argparse.ArgumentParser(description='fork or Thread')
        parser.add_argument('-m', '--m', action='store_true', help='Si se aplica se utiliza fork (por defecto se usa Thread)')
        args = parser.parse_args()
        return args