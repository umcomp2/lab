import socketserver
import pickle
import argparse
import calculator_operation


class TCPHandler(socketserver.BaseRequestHandler):

	def get_operation(self, operation=None, operands=None):
		response = None
		if operation == 'suma':
			response = calculator_operation.suma.delay(operands[0], operands[1])
		elif operation == 'resta':
			response = calculator_operation.resta.delay(operands[0], operands[1])
		elif operation == 'mult':
			response = calculator_operation.mult.delay(operands[0], operands[1])
		elif operation == 'div':
			response = calculator_operation.div.delay(operands[0], operands[1])
		elif operation == 'pot':
			response = calculator_operation.pot.delay(operands[0], operands[1])
		return response

	def handle(self):
		print('New client {} {}'.format(self.client_address[0], self.client_address[1]))

		data = self.request.recv(2048)
		data_decoded = pickle.loads(data)

		operation = self.get_operation(operation=data_decoded.get('operation'), operands=data_decoded.get('operands'))

		response = {
			'result': operation.get(),
			'success': operation.successful()
		}
		data_encoded = pickle.dumps(response)
		self.request.sendall(data_encoded)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Celery')

	parser.add_argument('-u', '--url', dest='url', default="localhost", required=True, type=str, metavar='Dirección Url',
						help='Ingrese dirección servidor.')
	parser.add_argument('-p', '--port', dest='port', default=9003, required=True, type=int, metavar='puerto',
						help='Ingrese puerto servidor.')

	options = parser.parse_args()

	socketserver.TCPServer.allow_reuse_address = True

	server = ThreadedTCPServer((options.url, options.port), TCPHandler)

	server.serve_forever()
