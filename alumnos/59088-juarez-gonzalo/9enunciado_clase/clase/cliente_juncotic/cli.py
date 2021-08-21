#!/usr/bin/python3
import sys
import socket
import getopt

def set_conn(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def close_conn(s):
    s.close()

def parse_args(args):
    optlist, args = getopt.getopt(args, "h:p:")
    host = ""
    port = 0
    for tup in optlist:
        key = tup[0].replace("-","")
        value = tup[1]
        if key == "h":
            host = value
        if key == "p":
            port = int(value)
    if not host or not port:
        raise ValueError("usage: %s -h [HOST] -p [PORT]" % __file__)
    return (host, port)

protocol = {
    "username": "hello",
    "email": "email",
    "password": "key",
    "exit": "exit",
}

def cli(s):
    user = {
            "username": "",
            "email": "",
            "password": "",
    }

    print("===== INICIO DEL CLI =====")
    for key in protocol:
        msg = input("Ingresar %s: " % key)
        if msg != "exit":
            user[key] = msg
            s.send((protocol[key] + "|" + user[key]).encode("utf8"))
            print(s.recv(1024).decode("utf8"))
        else:
            s.send(protocol[key].encode("utf8"))
            print(s.recv(1024).decode("utf8"))
    print("===== FIN DEL CLI =====")


if __name__ == "__main__":
    (host, port) = parse_args(sys.argv[1:])
    s = set_conn(host, port)
    cli(s)
    close_conn(s)
