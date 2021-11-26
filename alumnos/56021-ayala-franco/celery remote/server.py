import tasks
import asyncio
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", default="127.0.0.1", type=str, help="ip donde escuchar.")
parser.add_argument("-p", default=51007, type=int, help="puerto.")
args = parser.parse_args()

async def execute(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    operation = await reader.read(100)
    operation = operation.decode().split(":")
    operation[1] = float(operation[1])
    operation[2] = float(operation[2])
    print(operation)
    if operation[0] == "suma":
        result = tasks.add.delay(operation[1], operation[2]).get()
    if operation[0] == "rest":
        result = tasks.subtract.delay(operation[1], operation[2]).get()
    if operation[0] == "mult":
        result = tasks.multiply.delay(operation[1], operation[2]).get()
    if operation[0] == "div":
        result = tasks.divide.delay(operation[1], operation[2]).get()
    if operation[0] == "pot":
        result = tasks.power.delay(operation[1], operation[2]).get()
    
    writer.write(str(result).encode("ASCII"))
    await writer.drain()

async def main():
    server = await asyncio.start_server(execute, args.a, args.p)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())