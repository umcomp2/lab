import concurrent.futures, socket, os, sys

def servicio(s2, addr):
    print("Worker ", os.getpgid(), "atendiendo a ", addr)
    enviado = s2.recv(1024)
    respuesta = enviado.decode().upper()
    s2.send(respuesta.encode())
    print(enviado.decode())
    s2.close()

with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #... tenemos un pool "executor", y un socket que se llama "s"
        s.setsocket(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # get local machine name
        host = socket.gethostname()
        port = int(sys.argv[1])
        #bind to the port
        s.bind((host, port))
        s.listen(5)
        while True:
            s2, addr = s.accept()
            result = executor.sumbit(servicio, s2, addr)
