import socketserver
import subprocess
import pickle
import argparse


class TCPHandler(socketserver.BaseRequestHandler):

	def handle(self):
		print('New client {} {}'.format(self.client_address[0], self.client_address[1]))
		while True:

			data = self.request.recv(2048)

			if data == b'':
				print('Closed client {} {}'.format(self.client_address[0], self.client_address[1]))
				break

			if data:
				data = data.split()
				response = {}
				if b'rm' in data:
					response['status'] = 'ERROR'
					response['message'] = 'Comando no permitido'
				else:
					try:
						data_parsed = subprocess.run(data, capture_output=True)

						if data_parsed.returncode == 0:
							response['status'] = 'OK'
							response['message'] = data_parsed.stdout.decode()
						else:
							response['status'] = 'ERROR'
							response['message'] = data_parsed.stderr.decode()
					except Exception as e:
						response['status'] = 'ERROR'
						response['message'] = e.strerror
				data_encoded = pickle.dumps(response)
				self.request.sendall(data_encoded)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass


class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
	pass


def get_server_mode(mode=None, host=None, port=None):
	if mode == 'p':
		return ForkedTCPServer((host, port), TCPHandler)
	else:
		return ThreadedTCPServer((host, port), TCPHandler)


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Práctica - [remote_shell_serversocket]')

	parser.add_argument('-m', '--mode', dest='mode', default='t', required=True, type=str,
						metavar='protocolo', choices=['t', 'p'], help='Ingrese Modo.')

	options = parser.parse_args()

	socketserver.TCPServer.allow_reuse_address = True

	server = get_server_mode(mode=options.mode, host="localhost", port=9003)

	server.serve_forever()
