import socket
import argparse
import sys
from datetime import datetime

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Intro Sockets')
	parser.add_argument('-l', '--log', dest="log", required=False, default=None, type=str,
						metavar='Nombre archivo', help='Ingrese nombre del archivo log.')
	
	options = parser.parse_args()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()

	port = 9003

	s.connect((host, port))

	create_log = True if options.log else False

	print('Ingrese comando:')
	command = bytes(input(), "utf-8")

	while command != b'exit':

		s.send(command)
		response = s.recv(2048)
		response = response.decode("utf-8")
		print(response)

		if create_log:
			with open(options.log, 'a+') as f_log:

				f_log.write(str(datetime.now()))
				f_log.write('\n')
				f_log.write(response)

			f_log.close()

		command = bytes(input(), "utf-8")

	s.close()
	sys.exit()
