from socket import*

miSocket = socket()
miSocket.bind(('localhost', 8001))
miSocket.listen(5)

while True:
    conexion, addr = miSocket.accept()
    print('Nueva conexion establecida')
    print(addr)
    peticion = conexion.recv(1024)
    print(peticion.decode())

    conexion.send('Hola, te saludo desde el servidor!'.encode())
    conexion.close()
