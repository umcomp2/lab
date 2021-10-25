import socket
import sys
import subprocess
import signal
import asyncio


def handler(signum, frame):
    print("\rCerrando server...")
    server_socket.close()
    exit(0)

# Para el cierre del server
signal.signal(signal.SIGINT, handler)


# Core de la funcionalidad del server
async def handle_client(reader, writer):
    data = await reader.read(100)
    
    if not data:
        return None
    
    command = data.decode().split()
    returned = subprocess.run(command, capture_output=True)

    exit_code = bool(returned.returncode)

    if not exit_code:
        exit_stdout = str(returned.stdout, "utf-8")
        respuesta = bytes(f"OK\n{exit_stdout}", "utf-8")
    else:
        exit_stderr = str(returned.stderr, "utf-8")
        respuesta = bytes(f"ERROR\n{exit_stderr}", "utf-8")

    writer.write(respuesta)
    await writer.drain()

    return reader


async def recv_conn(reader, writer):
    conn = True
    while conn:
        conn = await handle_client(reader, writer)
    print(f"Conexion con {writer} finalizada...")


async def main():
    # Obtener de forma simple por CLI 
    HOST = "127.0.0.1"
    PORT = int(sys.argv[1])

    # Crear objeto socket del lado del server
    server_socket = await asyncio.start_server(recv_conn, HOST, PORT)

    async with server_socket:
        await server_socket.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
