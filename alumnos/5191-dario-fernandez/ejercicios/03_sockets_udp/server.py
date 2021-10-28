import socket
import argparse


def init_socket(protocol=None, port=None):
	if protocol == 'tcp':
		socket_type = socket.SOCK_STREAM
	else:
		socket_type = socket.SOCK_DGRAM

	sock = socket.socket(socket.AF_INET, socket_type)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(("", port))
	if protocol == 'tcp':
		sock.listen(5)
	return sock


def protocol_handler(sock=None, protocol=None):
	if protocol == 'tcp':
		new_conn, addr = sock.accept()
		data = new_conn.recv(2048)
	else:
		data, addr = sock.recvfrom(2048)

	return data, addr


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Sockets + stdin [tcp_udp]')
	parser.add_argument('-p', '--port', dest='port', default=9003, required=True, type=int, metavar='puerto',
						help='Ingrese puerto.')
	parser.add_argument('-t', '--protocol', dest='protocol', default='tcp', required=True, type=str,
						metavar='protocolo', choices=['tcp', 'udp'], help='Ingrese protocolo.')
	parser.add_argument('-f', '--file', dest='file', required=True, type=str,
						metavar='Nombre archivo', help='Ingrese nombre del archivo.')

	options = parser.parse_args()
	s = init_socket(protocol=options.protocol, port=options.port)

	while True:
		data, addr = protocol_handler(sock=s, protocol=options.protocol)

		print(data)

		with open(options.file, 'a+') as _file:
			_file.write(data.decode())
		_file.close()
		break
	s.close()
