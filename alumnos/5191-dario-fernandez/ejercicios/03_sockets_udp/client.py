import socket
import argparse
import sys


def init_socket(protocol=None, port=None):
	if protocol == 'tcp':
		socket_type = socket.SOCK_STREAM
	else:
		socket_type = socket.SOCK_DGRAM

	sock = socket.socket(socket.AF_INET, socket_type)
	sock.connect(("", port))
	return sock


def client_handler(sock=None, protocol=None, port=None):
	data = sys.stdin.readlines()

	if data:
		data = ' '.join(data).replace('\n','')
		if protocol == 'tcp':
			sock.send(data.encode())
		else:
			sock.sendto(data.encode(), ("", port))
	return None


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Sockets + stdin [tcp_udp]')
	parser.add_argument('-a', '--url', dest='url', default="", required=True, type=str, metavar='Dirección Url',
						help='Ingrese dirección servidor.')
	parser.add_argument('-p', '--port', dest='port', default=9003, required=True, type=int, metavar='puerto',
						help='Ingrese puerto servidor.')
	parser.add_argument('-t', '--protocol', dest='protocol', default='tcp', required=True, type=str,
						metavar='protocolo', choices=['tcp', 'udp'], help='Ingrese protocolo.')

	options = parser.parse_args()

	s = init_socket(protocol=options.protocol, port=options.port)

	while True:
		client_handler(sock=s, protocol=options.protocol, port=options.port)
		break

	s.close()
	sys.exit()
