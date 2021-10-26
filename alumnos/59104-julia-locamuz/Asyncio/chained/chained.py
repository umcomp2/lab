import asyncio
import random
import time

async def primera(n: int) -> str:

    # con gather se ejecutan concurrentemente cada corrutinas por cada parametro proporcionado

    i = random.randint(0, 10)
    print(f"primera({n}) esperando {i}s.")

    # will pause the current task and allow other tasks to be executed
    #   This function takes a single parameter which is a number of seconds, 
    # and returns a future which is not marked done yet but which will be when the specified
    # number of seconds have passed

    # las tasks (n tasks) le otorgan el procesamiento a otra task de la pila aqui 
    await asyncio.sleep(i)
    '''
    Lanzando primera
    primera(1) esperando 6s.
    Lanzando primera
    primera(2) esperando 5s.
    Lanzando primera
    primera(3) esperando 9s.
    
    '''
    
    result = f"result{n}-A"
    print(f"Retornando primera({n}) == {result}.")
    return result

async def segunda(n: int, arg: str) -> str:
    i = random.randint(0, 10)
    print(f"segunda{n, arg} esperando {i}s.")
    await asyncio.sleep(i)
    result = f"result{n}-B => {arg}"
    print(f"Retornando segunda{n, arg} => {result}.")
    return result

async def chain(n: int) -> None:
    start = time.perf_counter()
    print("Lanzando primera")
    # If the process the future ( creado a partir de el  await asyncio.sleep(i)) 
    # represents has finished and returned a value then 
    # the await statement immediately returns that value.
    prim = await primera(n)

    # se ejecuta el codigo anterior al sleep de cada task y se procede... 
    
    # recien cuando se devuelve un valor en la funcion a los i segundos 
    print("Lanzando Segunda")

    # le pasamos como resultado el result que es un objeto futuro que a los i segundos habra finalizado (f.done() returns True)

    segu = await segunda(n, prim)
    '''
    el del i mas pequeno: 
    Lanzando Segunda
    segunda(2, 'result2-A') esperando 3s.
    '''
    end = time.perf_counter() - start
    print(f"-->Encadenado result{n} => {segu} (tomó {end:0.2f} s).")

async def main(*args):
    await asyncio.gather(*(chain(n) for n in args))
    # asyncio.gather( chain(n1), chain(n2), chain(n3), ...)
    # default: asyncio.gather( chain(1), chain(2), chain(3))

if __name__ == "__main__":
    import sys
    random.seed(414)
    args = [1, 2, 3] if len(sys.argv) == 1 else map(int, sys.argv[1:])
    start = time.perf_counter()
    asyncio.run(main(*args))
    end = time.perf_counter() - start
    print(f"Program finished in {end:0.2f} seconds.")
