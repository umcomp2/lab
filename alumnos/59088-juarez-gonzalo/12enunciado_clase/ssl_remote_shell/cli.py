#!/usr/bin/python3
import socket
import ssl

import getopt
from datetime import datetime
import sys

from common import *

HOSTNAME = "localhost"
PORT = 8080

def ssl_cli_wrap(cli_s):

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    #context.verify_mode = ssl.CERT_REQUIRED
    #context.check_hostname = True
    context.load_default_certs()
    return context.wrap_socket(cli_s, server_hostname=HOSTNAME)

def set_cli():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s

def shell_loop(s, logger):
    print("STARTING CLI :) (EOF, empty command, or exit command to exit)\n")
    try:
        cmd = ""
        while cmd := input("$ "):
            if cmd == "exit":
                break
            send_msg(s, cmd)
            res = recv_msg(s)
            logger(cmd, res)
            print(res)
    except EOFError:
        pass
    send_msg(s, "exit")
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
    s = ssl_cli_wrap(s)
    s.connect((HOSTNAME, PORT))

    shell_loop(s, logger)
    s.close()
    close_logger()

if __name__ == "__main__":
    main()
