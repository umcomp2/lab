import argparse
import pickle
import socketserver
import crc_tasks


# Función argparse para definir host y puerto
def argumentos():
    parser = argparse.ArgumentParser(description='Server - Calculadora Celery')
    parser.add_argument('-ht', '--host', type=str, default='localhost',
                        help='Host de conexión para el server')
    parser.add_argument('-p', '--port', type=int, default=1234,
                        help='Puerto de conexión para el server')
    return parser.parse_args()


# Definir que tareas enviará el handler al Celery
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('Nueva conexión de dirección %s y puerto %d.\n' %
              (str(self.client_address[0]), self.client_address[1]))
        self.operation = self.request.recv(256)
        self.operation = pickle.loads(self.operation)
        self.operation = (self.operation).split()
        if self.operation[0] == 'suma':
            self.resultado = crc_tasks.suma.delay(float(self.operation[1]),
                                                  float(self.operation[2]))
        elif self.operation[0] == 'resta':
            self.resultado = crc_tasks.resta.delay(float(self.operation[1]),
                                                   float(self.operation[2]))
        elif self.operation[0] == 'mult':
            self.resultado = crc_tasks.mult.delay(float(self.operation[1]),
                                                  float(self.operation[2]))
        elif self.operation[0] == 'div':
            self.resultado = crc_tasks.div.delay(float(self.operation[1]),
                                                 float(self.operation[2]))
        elif self.operation[0] == 'pot':
            self.resultado = crc_tasks.pot.delay(float(self.operation[1]),
                                                 float(self.operation[2]))
        elif self.operation[0] == 'sqrt':
            self.resultado = crc_tasks.sqrt.delay(float(self.operation[1]))
        elif self.operation[0] == 'fact':
            self.resultado = crc_tasks.fact.delay(float(self.operation[1]))
        self.resultado_final = self.resultado.wait()
        self.request.sendall(pickle.dumps(self.resultado_final))
        print('Conexión con dirección %s y puerto %d finalizada. (%s, '
              'Resultado=%.2f)\n' % (str(self.client_address[0]),
                                     self.client_address[1], self.operation[0],
                                     self.resultado_final))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    # Definir host y puerto
    args = argumentos()
    host = args.host
    port = args.port
    print('Esperando conexiones...\n')
    with ThreadedTCPServer((host, port), MyTCPHandler) as server:
        server.serve_forever()
