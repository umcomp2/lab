import asyncio
import json


async def new_connection_handler(reader, writer):
    addr = writer.get_extra_info('peername')
    print('Nueva conexion desde {}'.format(addr))

    while True:
        # data = new_conn.recv(2048)
        data = await reader.read(2048)
        response = {}
        # print('data:', data)
        # print('type data:', type(data))
        if data:
            data = data.decode('utf-8')
            # data = data.decode('utf-8').split()
        print('data:', data)
        print('type data:', type(data))
        if data == b'':
            print('Closed client {} {}'.format(addr[0], addr[1]))
            break

        if 'rm' in data:
            response['status'] = 'ERROR'
            response['message'] = b'Comando no permitido'
        else:
            try:
                data_parsed = await asyncio.create_subprocess_shell(
                    data,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE)

                stdout, stderr = await data_parsed.communicate()
                print('stdout:', stdout)
                print('stderr:', stderr)

                if stdout:
                    response['status'] = 'OK'
                    response['message'] = stdout.decode('utf-8')
                    if stderr:
                        response['status'] = 'ERROR'
                        response['message'] = stderr.decode('utf-8')

            except Exception as e:
                response['status'] = 'ERROR'
                response['message'] = str(e.strerror)

            response_parsed = json.dumps(response)

            writer.write(response_parsed.encode('utf-8'))
            await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(new_connection_handler, host, port)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 9003

    asyncio.run(main())
