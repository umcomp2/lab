import socket
import subprocess
import asyncio
# import os


PORT = 2052
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = b"\n---DESCONECTADO---"




async def handle_client(reader, writer):
    print(f"---NUEVA CONEXIÓN---\n {writer} conectado con exito.")
    
    while True:
        msg = await reader.read(4096)
    
        if msg == DISCONNECT_MESSAGE: 
            writer.close()   
            break
        else:
            command = msg.split()
            process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            salida = stdout
            writer.write(bytes(salida, FORMAT))
            await writer.drain()
            error = stderr
            writer.write(bytes(error, FORMAT))
            await writer.drain()

            
        
  

async def start():
    server = await asyncio.start_server(handle_client,SERVER, PORT)
    async with server:
        await server.serve_forever()


print("---STARTING--- El servidor ha comenzado...")
asyncio.run(start())



