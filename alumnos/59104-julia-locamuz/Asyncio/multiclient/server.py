import pickle
import subprocess
import asyncio

async def handle_connection(reader, writer):
    connected = True
    while connected:
        connection = await handle_client(reader, writer)

async def handle_client(reader, writer):
    connected = True
    data = await reader.read(100)
    if not data:
        return None
    message = pickle.loads(data)
    out = subprocess.run(message.split(), capture_output=True)
    exit = bool(out.returncode)

    if exit == False:      
        send_message = pickle.dumps(out.stdout) 
        writer.write(send_message)
        await writer.drain()
    else:
        error_message = pickle.dumps(out.stderr)
        writer.write(error_message)
        await writer.drain()
    return reader

async def main():    
    server = await asyncio.start_server(
        handle_connection, '127.0.0.1', 8888)  
    async with server:
        await server.serve_forever()


asyncio.run(main())