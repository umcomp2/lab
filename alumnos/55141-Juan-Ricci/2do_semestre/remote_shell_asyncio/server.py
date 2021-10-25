#!/usr/bin/python3
import subprocess as sp
import asyncio


async def handle_shell(reader, writer):
    while True:
        data = await reader.read(100)
        recv_data = data[:-2]
        message = data.decode()
        if message == 'exit\r\n':
            break
        addr = writer.get_extra_info('peername')
        print(f"Received {message!r} from {addr!r}")
        process = sp.Popen([recv_data], shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = process.communicate()
        if stdout != b'':
            print(f"Sending: {stdout}")
            writer.write(stdout)
        else:
            print(f"Sending error: {stderr}")
            writer.write(stderr)
        respuesta = b'Input another command ([exit] to close connection): '
        writer.write(respuesta)
        await writer.drain()
    print("Closing connecton!")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_shell, '127.0.0.1', 8888
    )
    async with server:
        await server.serve_forever()
        
asyncio.run(main())