import socket
import argparse
import sys
import pickle


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Celery')
    parser.add_argument('-u', '--url', dest='url', default="", required=True, type=str, metavar='Dirección Url',
                        help='Ingrese dirección servidor.')
    parser.add_argument('-p', '--port', dest='port', default=9003, required=True, type=int, metavar='puerto',
                        help='Ingrese puerto servidor.')
    parser.add_argument('-o', '--operation', dest='operation', required=True, type=str, metavar='operacion',
                        choices=['suma', 'resta', 'mult', 'div', 'pot'], help='Ingrese Operación.')
    parser.add_argument('-n', '--number1', dest='first', required=True, type=int, metavar='primer operando',
                        help='Ingrese primer operando.')
    parser.add_argument('-m', '--number2', dest='second', required=True, type=int, metavar='segundo operando',
                        help='Ingrese segundo operando.')

    options = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = options.url, 9003

    s.connect((host, port))

    calc_operation = {
        'operation': options.operation,
        'operands': [options.first, options.second]
    }

    data_encoded = pickle.dumps(calc_operation)
    s.send(data_encoded)
    response = s.recv(2048)

    response_decoded = pickle.loads(response)

    if response_decoded.get('success'):
        print('El resultado es: {}'.format(response_decoded.get('result')))
    else:
        print('Hubo un error en procesar el resultado')

    s.close()
    sys.exit()
