import socket

from Protocol import Protocol

RECV_SIZE = 1 << 12

# clases que siguen una misma interfaz (Protocol_SV)
# y estarian en archivos distintos en un lenguaje compilado
# o en un proyecto mas grande

# clase que esta a modo de interfaz
# mas bien a forma de documentacion
# porque en lenguaje con tipado dinamico
# no importa a nivel funcionamiento
class Protocol_SV(Protocol):
    def __init__(self, port, host=""):
        pass

    def recv(self, msg):
        pass

    def send(self, msg):
        pass

    def __del__(self):
        pass

class UDP_SV(Protocol_SV):
    def __init__(self, port, host=""):
        self.client_addr = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR | socket.SO_REUSEPORT, 1)
        self.sock.bind((host, port))

    def recv(self):
        if not self.client_addr:
            msg, self.client_addr = self.sock.recvfrom(RECV_SIZE)
        else:
            # de manera que actue como TCP de una sola conexion
            msg, _ = self.sock.recvfrom(RECV_SIZE)
        return msg.decode("utf8")

    def send(self, msg):
        if not self.client_addr:
            raise ValueError("Error en UDP_SV::send(): No existe cliente al cual enviar el mensaje")
        msg_b = bytes(msg, "utf8")
        sent = 0
        while sent < len(msg_b):
            sent += self.sock.sendto(msg_b[sent:], self.client_addr)

    def __del__(self):
        self.sock.close()
        self.sock = None

class TCP_SV(Protocol_SV):
    def __init__(self, port, host=""):
        self.client_sock = None
        self.client_addr = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR | socket.SO_REUSEPORT, 1)
        self.sock.bind((host, port))
        self.sock.listen(1)

    def recv(self):
        if not self.client_sock:
            self.client_sock, self.client_addr = self.sock.accept()
            # es una aplicacion de una sola conexion
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.sock = None
        msg = self.client_sock.recv(RECV_SIZE)
        return msg.decode("utf8")

    def send(self, msg):
        if not self.client_sock:
            raise ValueError("Error en TCP_SV::send(): No existe conexion con el cliente")
        msg_b = bytes(msg, "utf8")
        sent = 0
        while sent < len(msg_b):
            sent += self.client_sock.send(msg_b[sent:])

    def __del__(self):
        if self.sock:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.sock = None
        if self.client_sock:
            self.client_sock.shutdown(socket.SHUT_RDWR)
            self.client_sock.close()
            self.client_sock = None
