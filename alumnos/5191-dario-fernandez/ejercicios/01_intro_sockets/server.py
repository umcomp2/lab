# -*- coding: utf-8 -*-
import socket
import subprocess

if __name__ == '__main__':

	host = socket.gethostname()
	port = 9003
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))
	s.listen(5)

	while True:
		new_conn, addr = s.accept()
		print('Nueva conexion desde {}'.format(addr))

		while new_conn:
			data = new_conn.recv(2048)
			if data:
				data = data.split()

				if b'rm' in data:
					response = 'ERROR\n Comando no permitido'
				else:
					try:
						data_parsed = subprocess.run(data, capture_output=True)
						response_ok = data_parsed.stdout
						response_error = data_parsed.stderr

						if data_parsed.returncode == 0:
							status_code = 'OK\n'
							response = "{} {}".format(status_code, data_parsed.stdout.decode("utf-8"))
						else:
							status_code = 'ERROR\n'
							response = "{} {}".format(status_code, data_parsed.stderr.decode("utf-8"))
					except Exception as e:
						status_code = 'ERROR\n'
						response = "{} {}".format(status_code, str(e.strerror))

				new_conn.send(bytes(response, "utf-8"))

		s.close()
