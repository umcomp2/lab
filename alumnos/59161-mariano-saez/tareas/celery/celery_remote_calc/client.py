import socket


if __name__ == "__main__":
    import argparse as ap

    parser = ap.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        type=str,
        help="IP del servidor. localhost es el default.",
        default="0.0.0.0",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="Puerto donde escucha el servidor. 9999 es el default.",
        default=9999,
    )
    parser.add_argument(
        "-o",
        "--operation",
        type=str,
        help="Nombre de la operacion.",
        choices=[
            "suma",
            "resta",
            "mult",
            "div",
            "pot",
        ],
    )
    parser.add_argument(
        "n",
        type=int,
        help="Primer operando",
    )
    parser.add_argument(
        "m",
        type=int,
        help="Segundo operando",
    )
    args = parser.parse_args()

    ADDR = args.address
    PORT = args.port
    OP = args.operation
    N = args.n
    M = args.m

    data = bytes(f"{OP} {N} {M}", encoding="utf-8")

    s = socket.socket()
    s.connect((ADDR, PORT))
    s.send(data)
    result = s.recv(1024)
    print(str(result, encoding="utf-8"))