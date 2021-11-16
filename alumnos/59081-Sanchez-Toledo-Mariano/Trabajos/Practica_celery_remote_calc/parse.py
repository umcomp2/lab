import argparse

def parseServer():
    parser = argparse.ArgumentParser(description='Server options')
    parser.add_argument('-i', '--ip', type=str, help='Introduce ip to host server')
    parser.add_argument('-p', '--port', type=int, help='Introduce port to host server')
    args = parser.parse_args()
    return args

def parseClient():
    parser = argparse.ArgumentParser(description='Client options')
    parser.add_argument('-i', '--ip', type=str, help='Introduce ip to connect to server')
    parser.add_argument('-p', '--port', type=int, help='Introduce port to connect to server')
    parser.add_argument('-o', '--operation', type=str, help='Introduce operation to perform')
    parser.add_argument('-n', '--num1', type=int, help='Introduce first number')
    parser.add_argument('-m', '--num2', type=int, help='Introduce second number')
    args = parser.parse_args()
    return args