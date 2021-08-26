import socket

from Protocol import Protocol

# clases que siguen una misma interfaz (Protocol_CLI)
# y estarian en archivos distintos en un lenguaje compilado
# o en un proyecto mas grande

RECV_SIZE = 1 << 12

# clase que esta a modo de interfaz
# mas bien a forma de documentacion
# porque en lenguaje con tipado dinamico
# no importa a nivel funcionamiento
class Protocol_CLI(Protocol):
    def __init__(self, sv_address, sv_port):
        pass

    def send(self, msg):
        pass

    def recv(self):
        pass

    def __del__(self):
        pass

class TCP_CLI:
    def __init__(self, sv_address, sv_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR | socket.SO_REUSEPORT, 1)
        self.sock.connect((sv_address, sv_port))

    def send(self, msg):
        msg_b = bytes(msg, "utf8")
        sent = 0
        while sent < len(msg_b):
            sent += self.sock.send(msg_b[sent:])

    def recv(self):
        msg = self.sock.recv()
        return msg.decode("utf8")

    def __del__(self):
        self.sock.send(b"") # EOF
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.sock = None

class UDP_CLI:
    def __init__(self, sv_address, sv_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR | socket.SO_REUSEPORT, 1)
        self.sv_address = sv_address
        self.sv_port = sv_port

    def send(self, msg):
        msg_b = bytes(msg, "utf8")
        sent = 0
        while sent < len(msg_b):
            sent += self.sock.sendto(msg_b[sent:], (self.sv_address, self.sv_port))

    def recv(self):
        msg = self.sock.recvfrom(RECV_SIZE)
        return msg.decode("utf8")

    def __del__(self):
        self.sock.sendto(b"", (self.sv_address, self.sv_port)) # EOF
        self.sock.close()
        self.sock = None
        self.sv_address = ""
        self.sv_port = 0
