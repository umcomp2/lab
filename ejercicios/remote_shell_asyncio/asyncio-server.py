import subprocess as sp
import argparse
import asyncio 

parserito_s = argparse.ArgumentParser(description='socket server')
parserito_s.add_argument('-p', '--port', dest = "puerto", type = int, required = True, help = "Puerto utilizado")

args = parserito_s.parse_args()

async def handle(reader, writer):
    print("Conexion establecida")
    while True:

        data = await reader.read(4096)
        data2 = str(data, "utf-8")

        if data2 != "exit":
            datos = data2.split()
            fin = sp.Popen(datos, stdout=sp.PIPE, universal_newlines=True, stderr=sp.PIPE)
            output_full = fin.communicate()
            salida = output_full[0]
            writer.write(bytes(salida, "utf-8"))
            await writer.drain()
            error = output_full[1]
            writer.write(bytes(error, "utf-8"))
            await writer.drain()
        
        elif data2 == "exit":
            writer.close()
            break

async def main():
    id = "0.0.0.0"
    puerto = args.puerto
    server = await asyncio.start_server(handle, id, puerto)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
