#!/usr/bin/python3
import socket

import getopt
from datetime import datetime
import sys

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
    # bytearray != bytes ?? python3
    return bytes(msg[:-len(MSG_TERM)])

def send_cmd(s, cmd):
    acc = 0
    sent = 0
    cmd += MSG_TERM
    while sent := s.send(cmd[acc:]):
        acc += sent

def shell_loop(s, logger):
    print("STARTING CLI :) (EOF, empty command, or exit command to exit)\n")
    try:
        cmd = ""
        while cmd := input("$ "):
            if cmd == "exit":
                break
            send_cmd(s, bytes(cmd, "utf8"))
            res = recv_response(s).decode("utf8")
            logger(cmd, res)
            print(res)
    except EOFError:
        pass
    send_cmd(s, bytes("exit", "utf8"))
    print("\nEXITING CLI :(")
    s.close()

def get_logger(file=None):
    if not file:
        # stubs
        def logger(cmd, res):
            return
        def close_logger():
            return
    else:
        filehandle = open(file, "w")
        def logger(cmd, res):
            date = str(datetime.now())
            filehandle.write("[ %s ]: %s\n%s\n" % (
                                date,
                                cmd,
                                res,
                                ))
            return
        def close_logger():
            filehandle.close()
            return
    return logger, close_logger

def parse_args(args):
    optlist, args = getopt.getopt(args, "l:")
    filepath = ""
    for opt in optlist:
        if opt[0] == "-l":
            filepath = opt[1]
    return filepath

def main():
    filepath = parse_args(sys.argv[1:])
    logger, close_logger = get_logger(filepath)
    s = set_cli()
    shell_loop(s, logger)
    close_logger()

if __name__ == "__main__":
    main()
