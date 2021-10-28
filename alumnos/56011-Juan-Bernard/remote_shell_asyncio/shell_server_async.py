import argparse
import asyncio
import subprocess as sp

# Función argparse para definir host y puerto
def argumentos():
    parser = argparse.ArgumentParser(description='Shell Server Asyncio - Comandos')
    parser.add_argument('-ht', '--host', type=str, default='127.0.0.1',
                        help='Host de conexión para el server')
    parser.add_argument('-p', '--port', type=int, default=1234,
                        help='Puerto de conexión para el server')
    return parser.parse_args()

async def comandos(reader, writer):
    writer.write('Conexión correcta. Puede proceder.'.encode('utf-8'))
    await writer.drain()
    while True:
        comando_1 = await reader.read(256)
        if not comando_1:
            break
        comando_2 = comando_1.decode('utf-8')
        print('Se recibió: ',comando_2)
        comando_3 = sp.Popen(comando_2, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        stdout, stderr = comando_3.communicate()
        if stdout:
            writer.write(b'OK\n%s' % stdout)
        elif stderr:
            writer.write(b'ERROR\n%s' % stderr)
        await writer.drain()
    writer.close()
    t = asyncio.current_task()
    print(f"Cerrando Tarea: {t}")

async def main():
    # Definir host y puerto
    args = argumentos()
    host = args.host
    port = args.port
    # Arrancar el server
    server = await asyncio.start_server(comandos, host, port)
    print('Esperando conexiones...')
    async with server:
        print(f"Tareas:\n{asyncio.all_tasks()}")
        await server.serve_forever()        


asyncio.run(main())
