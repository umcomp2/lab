import socket
import subprocess
import threading
import pickle

def new_connection_handler(new_conn, addr):
	print('Nueva conexion desde {}'.format(addr))
	
	while True:
		data = new_conn.recv(2048)

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
			new_conn.send(data_encoded)

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
