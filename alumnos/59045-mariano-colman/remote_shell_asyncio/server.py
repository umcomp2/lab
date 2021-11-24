import subprocess, asyncio, sys, os

async def consultas(reader, writer):
    directorio = os.getcwd()
    dir = directorio.encode()
    print(dir)
    writer.write(dir)
    await writer.drain()
    while True:
        comando = await reader.read(1024)
        comando2 = comando.decode()
        if comando2.lower() == "exit":
            print("\n[+]CONEXION FINALIZADA")
            break
        else:
            try:
                output = subprocess.getoutput(comando2)
                rta = f"OK\n{output}"
            except subprocess.CalledProcessError as error:
                rta = f"ERROR\n{output}"
            writer.write(rta.encode('utf-8'))
            await writer.drain()
    writer.close()

async def main():
    HOST = 'localhost'
    PORT = int(sys.argv[1])
    directorio = os.getcwd()
    servidor = await asyncio.start_server(consultas, HOST, PORT)
    print("[+]SERVIDOR INICIADO!")
    async with servidor:
        await servidor.serve_forever()


asyncio.run(main())