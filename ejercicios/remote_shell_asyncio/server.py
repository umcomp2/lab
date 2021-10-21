import socket
import subprocess 
import asyncio
import os

HEADER = 64
PORT = 8888
SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


async def handle_client(reader, writer):
    print(f"[NEW CONNECTION]")

    while True:
        data = await reader.read(1024)
        if not data:
            print(f"[CLOSE CONNECTION]")
            break
        print("[RECEIVED]")

        if data == DISCONNECT_MESSAGE:
            writer.close()
            break

        data2 = data.split()
        returned = subprocess.run(data2, capture_output=True)

        exit_code = bool(returned.returncode)
        if not exit_code:
            exit_stdout = str(returned.stdout,"utf-8")
            respuesta = bytes(f"OK\n {exit_stdout}", "utf-8")
            writer.write(respuesta)
            await writer.drain()
        else:
            exit_stderr = str(returned.stderr,"utf-8")
            respuesta = bytes(f"ERROR\n{exit_stderr}", "utf-8")
            writer.write(respuesta)
            await writer.drain()

        






async def start():
    server = await asyncio.start_server(
    handle_client, "127.0.1.1", 8888)
    addr = server.sockets[0].getsockname()
    print("LISTENING ON: ", addr)

    async with server:
        await server.serve_forever()

asyncio.run(start())