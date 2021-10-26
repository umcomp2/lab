import socket
import sys
import subprocess
import asyncio


async def client_handler(conn, addr):
        loop = asyncio.get_event_loop()
        print(f"Nueva conexion establecida[cliente:{addr}]")
        connected  = True
        while connected:
            msg = (await loop.sock_recv(conn,4096)).decode('utf-8')
            if msg == '!DISCONNECT':
                conn.close()
                print(f"Conexion finalizada[cliente:{addr}]")
                break

            cmd = msg.split()
            estado_cmd = subprocess.run(cmd,capture_output=True)
            if estado_cmd.returncode == 0:
                correct_output = estado_cmd.stdout.decode("utf-8")
                msg_back = bytes(f"OK\n{correct_output}", "utf-8")
                await loop.sock_sendall(conn,msg_back)
            else:
                error_output = estado_cmd.stderr.decode("utf-8")
                msg_back = bytes(f"ERROR\n{error_output}", "utf-8")
                await loop.sock_sendall(conn,msg_back)
            


#Esta funcion inizializa el server para comenzar a escuchar conexiones
async def run_server(ip,port):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen()
    server.setblocking(False)
    print(F"Servidor inizializado y escuchando en {SERVER}")
    loop = asyncio.get_event_loop()
    while True:
        conn, addr = await loop.sock_accept(server)
        loop.create_task(client_handler(conn,addr))

if __name__ == "__main__":
    PORT = int(sys.argv[1])
    SERVER= "127.0.0.1"
    print("Inizializando Servidor....")
    asyncio.run(run_server(SERVER,PORT))