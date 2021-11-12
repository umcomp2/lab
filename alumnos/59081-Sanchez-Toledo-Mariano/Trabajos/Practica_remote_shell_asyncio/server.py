from socket import *
from subprocess import *
from threading import *
import pickle
import asyncio


class ServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Conection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        comando = pickle.loads(data)

        if comando == 'stop':
            self.transport.close()


        print('Comando recibido:\n', comando)
        out = getoutput(comando)
        newout = pickle.dumps(out)
        self.transport.write(newout)

        #self.transport.close()


async def main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: ServerProtocol(),
        'localhost',
        9090
    )
    
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())