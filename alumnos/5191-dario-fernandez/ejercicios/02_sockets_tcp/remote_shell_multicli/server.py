import socket
import subprocess
import threading

def new_connection_handler(new_conn, addr):
	print('Nueva conexion desde {}'.format(addr))
	
	while True:
		data = new_conn.recv(2048)

		if data:
			data = data.split()

			if b'rm' in data:
				response = 'ERROR\n Comando no permitido'
			else:			
				try:
					data_parsed = subprocess.run(data, capture_output=True)

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


if __name__ == '__main__':

	host = socket.gethostname()
	port = 9003
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))
	s.listen(5)

	print('Iniciando Servidor')
	while True:
		new_conn, addr = s.accept()
		
		th = threading.Thread(target=new_connection_handler, args=(new_conn, addr))
		th.start()
