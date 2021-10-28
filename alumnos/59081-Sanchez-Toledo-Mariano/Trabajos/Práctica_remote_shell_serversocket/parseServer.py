import argparse

class Parser:
    def parser():
        parser = argparse.ArgumentParser(description='Fork or Thread')
        parser.add_argument('-m', '--mode', type=str, help='t para thread y p para fork')
        args = parser.parse_args()
        return args