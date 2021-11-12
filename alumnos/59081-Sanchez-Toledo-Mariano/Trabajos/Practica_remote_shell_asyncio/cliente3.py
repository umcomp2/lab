import asyncio
import pickle

class ClientProtocol(asyncio.Protocol):
    def __init__(self, on_con_lost):
        self.command = ''
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        self.transport = transport
        self.command = str(input('Ingrese Comando: '))
        transport.write(pickle.dumps(self.command))
        print('Data sent {!r}'.format(self.command))

    def data_received(self, data):
        print('Data received: {!r}'.format(pickle.loads(data)))
        self.connection_made(self.transport)

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)

async def main():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()

    #command = str(input('Ingrese comando: '))

    transport, protocol =  await loop.create_connection(
        lambda: ClientProtocol(on_con_lost),
        'localhost',
        9090
    )

    try:
        await on_con_lost
    finally:
        transport.close()

if __name__ == '__main__':
    asyncio.run(main())