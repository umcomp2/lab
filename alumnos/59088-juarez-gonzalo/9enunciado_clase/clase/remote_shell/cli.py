#!/usr/bin/python3
import socket

HOSTNAME = "localhost"
PORT = 8080

MAXINPUTSIZE = 1024
MSG_TERM = b"\r\n\r\n"

def set_cli():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOSTNAME, PORT))
    return s

def recv_response(s):
    msg = bytearray()
    while len(msg) < len(MSG_TERM) or\
        msg[-len(MSG_TERM):] != MSG_TERM:
            msg += s.recv(MAXINPUTSIZE)
    # bytearray not considered bytes object?? python3
    return bytes(msg[:-len(MSG_TERM)])

def send_cmd(s, cmd):
    acc = 0
    sent = 0
    cmd += MSG_TERM
    while sent := s.send(cmd[acc:]):
        acc += sent

def shell_loop(s):
    print("STARTING CLI :)\n")
    try:
        cmd = ""
        while cmd := input("$ "):
            if cmd == "exit":
                break
            send_cmd(s, bytes(cmd, "utf8"))
            res = recv_response(s)
            print(res.decode("utf8"))
    except EOFError:
        pass
    send_cmd(s, bytes("exit", "utf8"))
    print("\nEXITING CLI :(")
    s.close()

def main():
    s = set_cli()
    shell_loop(s)


if __name__ == "__main__":
    main()
