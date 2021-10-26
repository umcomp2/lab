import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

'''

SINCRONICO 

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")'''

async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))

    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

# el await larga la corrutina pero de manera sincronica, hay que envolverlo en tasks 
# para que sea concurrente 

asyncio.run(main())