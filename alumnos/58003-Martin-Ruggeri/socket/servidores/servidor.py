import socket

#esta funcion va a jenerar un nuevo socket con los valores por default
mi_socket = socket.socket()
#voy a establecer la conexion
#el primer valor sera el host, y el segundo en que puerto estara escuchando el socket
mi_socket.bind(('localhost', 8000))
# vamos a establecer la cantidad de peticiones que puede manejar nuestro socket en cola
mi_socket.listen(5)

while True:
    # vamos a aceptar las peticiones del cliente
    # nos va a retornar 2 valores (la conexion y la direccion)
    conexion, addr = mi_socket.accept()
    print("Nueva conexion establecida")
    print(f"la direccion de la cual se ha hecho la peticion", addr)
    # obtenemos lo que el cliente nos esta enviando
    peticion = conexion.recv(1024)
    print(peticion)
    #vamos a enviar un mensaje al cliente
    conexion.send(bytes("Hola, te saludo desde el servidor", encoding = "utf-8"))
    #cerramos la conexion con el cliente
    conexion.close()
