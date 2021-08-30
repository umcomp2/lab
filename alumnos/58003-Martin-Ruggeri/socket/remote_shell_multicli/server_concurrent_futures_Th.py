import concurrent.futures, socket, os, sys, subprocess


def servicio(conn, addr):
    print("Worker ", os.getpgid(), "atendiendo a ", addr)
    while conn:
        data = str(conn.recv(4096), "utf-8")
        command = data.split()
        returned = subprocess.run(command, capture_output=True)
        exit_code = bool(returned.returncode)

        if not exit_code:
            exit_stdout = str(returned.stdout, "utf-8")
            respuesta = bytes(f"OK\n{exit_stdout}", "utf-8")
        else:
            exit_stderr = str(returned.stderr, "utf-8")
            respuesta = bytes(f"ERROR\n{exit_stderr}", "utf-8")

        conn.send(respuesta)

    conn.close()
    print(f"Conexion con {addr} finalizada...")


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #... tenemos un pool "executor", y un socket que se llama "s"
        s.setsocket(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # get local machine name
        host = "127.0.0.1"
        port = int(sys.argv[1])
        # bind to the port
        s.bind((host, port))
        s.listen(5)
        while True:
            s2, addr = s.accept()
            result = executor.sumbit(servicio, s2, addr)
