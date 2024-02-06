import socket
from calc import *

FOO = {
    "suma" : suma,
    "resta" : resta,
    "mult" : mult,
    "div" : div,
    "pot" : pot,
}


if __name__ == "__main__":
    import argparse as ap

    parser = ap.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        type=str,
        help="IP host donde atender. 0.0.0.0 es el default.",
        default="0.0.0.0",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="Puerto donde atender. 9999 es el default.",
        default=9999,
    )
    args = parser.parse_args()

    ADDR = args.address
    PORT = args.port

    s = socket.socket()
    s.bind((ADDR, PORT))
    s.listen()

    while True:
        conn, client = s.accept()
        data = str(conn.recv(1024), encoding="utf-8").split()
        
        op = data[0]
        n = float(data[1])
        m = float(data[2])

        async_op = FOO[op].delay(n, m)

        result = str(async_op.get(timeout=5))

        conn.send(bytes(result, encoding="utf-8"))
        conn.close()

