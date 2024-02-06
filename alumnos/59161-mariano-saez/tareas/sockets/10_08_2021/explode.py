import socket, os

# Tener dos procesos
os.fork()

# Tener cuatro procesos
os.fork()

# Tirar conexiones al server
for i in range(25):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 35001))