import pickle

MAXINPUTSIZE = 4096
MSG_TERM = b"\r\n\r\n"

def send_msg(s, msg):
    msg = bytes(msg, "utf8")
    msg = pickle.dumps(msg)

    msg += MSG_TERM
    acc = 0
    while (acc := acc + s.send(msg[acc:])) < len(msg):
        continue

def recv_msg(s):
    msg = bytearray()
    while len(msg) < len(MSG_TERM) or\
            msg[-len(MSG_TERM):] != MSG_TERM:
        msg += s.recv(MAXINPUTSIZE)

    # bytearray != bytes ?? python3
    msg = pickle.loads(msg[:-len(MSG_TERM)])
    return msg.decode("utf8")
