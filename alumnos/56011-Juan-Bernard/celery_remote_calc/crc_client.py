import argparse
import pickle
import socket


# Función argparse para definir host, puerto, operación y operandos
def argumentos():
    parser = argparse.ArgumentParser(description='Client - Calculadora Celery')
    parser.add_argument('-ht', '--host', type=str, default='localhost',
                        help='Host de conexión para el server')
    parser.add_argument('-p', '--port', type=int, default=1234,
                        help='Puerto de conexión para el server')
    parser.add_argument('-o', '--operation', type=str, default='suma',
                        help='Operación a realizar')
    parser.add_argument('-n', '--n_operand', type=str, default='1',
                        help='Primer operando')
    parser.add_argument('-m', '--m_operand', type=str, default='1',
                        help='Segundo operando')
    return parser.parse_args()


sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Definir host y puerto
args = argumentos()
host = args.host
port = args.port
# Conectar al host a través del puerto señalado y enviar datos
sockt.connect((host, port))
tarea = args.operation + ' ' + args.n_operand + ' ' + args.m_operand
sockt.sendall(pickle.dumps(tarea))
# Recibir y mostrar respuesta
resultado = sockt.recv(1024)
n_resultado = pickle.loads(resultado)
print('Resultado: %.2f' % n_resultado)
print('Conexión terminada.')
