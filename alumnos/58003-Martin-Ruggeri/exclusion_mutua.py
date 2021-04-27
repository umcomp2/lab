import argparse


parser = argparse.ArgumentParser(description='Calculadora python')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-s', '--suma', action='store_true',
                   default=False, help="suma de dos numeros")
group.add_argument('-r', '--resta', action='store_true',
                   default=False, help="resta de dos numeros")
group.add_argument('-m', '--multi', action='store_true',
                   default=False, help="multi de dos numeros")
group.add_argument('-d', '--divi', action='store_true',
                   default=False, help="divi de dos numeros")
