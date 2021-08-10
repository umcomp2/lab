#!/usr/bin/python3
import socket

PORT = 8000
ADDR = ""

RECV_BUFF = 1 << 15


def cmd_loop(client_s):
    cmd = b""

    # loop se termina cuando input == ""
    while cmd := input(">> "):
        client_s.send(cmd.encode("utf-8"))
        msg = client_s.recv(RECV_BUFF)
        print(msg.decode("utf-8"))

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDR, PORT))
    cmd_loop(s)
    s.close()

if __name__ == "__main__":
    main()
