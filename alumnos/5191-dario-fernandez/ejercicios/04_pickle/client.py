import socket
import argparse
import sys
from datetime import datetime
import pickle

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Sockets TCP - Remote Shell Multicli ')
	parser.add_argument('-l', '--log', dest="log", required=False, default=None, type=str,
						metavar='Nombre archivo', help='Ingrese nombre del archivo log.')
	
	options = parser.parse_args()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()

	port = 9003

	s.connect((host, port))

	create_log = True if options.log else False

	while True:
		print('Ingrese comando:')
		command = bytes(input(), "utf-8")
		if command == b'exit':
			break
		
		s.send(command)
		response = s.recv(2048)
		response = pickle.loads(response)

		print(response)

		if create_log:
			with open(options.log, 'a+') as f_log:
				f_log.write(str(datetime.now()))
				f_log.write('\n')
				f_log.write(response['status'])
				f_log.write('\n')
				f_log.write(response['message'])

			f_log.close()

	s.close()
	sys.exit()
