import subprocess
import asyncio

async def execute(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    while True:
        command = await reader.read(100)
        command = command.decode()
        result = subprocess.run(command, capture_output=True, encoding="UTF-8")
        response = f"=== Execution Result: {str(result.returncode)} ===\n{result.stdout}=== Execution End ==="
        writer.write(bytes(response, "UTF-8"))
        await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(execute, "127.0.0.1", 51007)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
