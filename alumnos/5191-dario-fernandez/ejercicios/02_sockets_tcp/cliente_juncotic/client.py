import socket
import argparse
import sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Sockets TCP - Juncotic')
    parser.add_argument('-u', '--host', dest="host", required=True, default="", type=str,
                        metavar='host', help='Ingrese URL.')
    parser.add_argument('-p', '--port', dest="port", required=True, type=int, metavar='puerto',
                        help='Ingrese puerto.')

    options = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()

    s.connect((options.host, options.port))

    allowed_commands = {
        'hello': {
            'value': 'nombre'
        },
        'email': {
            'value': 'correo electronico'
        },
        'key': {
            'value': 'clave'
        }
    }

    code_errors = {
        "200": "OK",
        "400": "Comando válido, pero fuera de secuencia.",
        "500": "Comando inválido.",
        "404": "Clave errónea.",
        "405": "Cadena nula."
    }

    for cmd in allowed_commands:
        status_code = None

        while status_code != "200":
            command = input(("Ingrese {} ").format(allowed_commands[cmd].get('value')))

            s.send(("{}|{}".format(cmd, command).encode('ascii')))
            status_code = s.recv(1024).decode('ascii')

            # print('Status code', status_code)
            print(code_errors[status_code])

    s.send("exit".encode('ascii'))

    s.close()
    sys.exit()
