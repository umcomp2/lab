MAXINPUTSIZE = 4096
MSG_TERM = b"\r\n\r\n"

def send_msg(s, msg):
    acc = 0
    msg += MSG_TERM
    while (acc := acc + s.send(msg[acc:])) < len(msg):
        continue

def recv_msg(s):
    msg = bytearray()
    while len(msg) < len(MSG_TERM) or\
            msg[-len(MSG_TERM):] != MSG_TERM:
        msg += s.recv(MAXINPUTSIZE)
    # bytearray != bytes ?? python3
    return bytes(msg[:-len(MSG_TERM)])
