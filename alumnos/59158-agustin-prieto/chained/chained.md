import asyncio
import random
import time

    ## Se define un corrutina que recibe un entero como input y devuelve un str
async def primera(n: int) -> str:
    i = random.randint(0, 10)
    print(f"primera({n}) esperando {i}s.")

    ## Con el await dormimos la corrutina por "i" segundos
    ## permitiendo que se ejecuten otras coroutines
    await asyncio.sleep(i)

   
    result = f"result{n}-A"
    print(f"Retornando primera({n}) == {result}.")
    return result


    ## Se define un corrutina que recibe un entero como input y el resultado de la primera
    ## corrutina y devuelve un str
async def segunda(n: int, arg: str) -> str:
    i = random.randint(0, 10)
    print(f"segunda{n, arg} esperando {i}s.")

    ## Con el await dormimos la corrutina por "i" segundos
    ## permitiendo que se ejecuten otras coroutines
    await asyncio.sleep(i)
    result = f"result{n}-B => {arg}"
    print(f"Retornando segunda{n, arg} => {result}.")
    return result

async def chain(n: int) -> None:

    
    start = time.perf_counter()
    print("Lanzando primera")
    ## Llama la corrutina "primera"
    prim = await primera(n)
    print("Lanzando Segunda")
    ## Llama la corrutina "segunda"
    segu = await segunda(n, prim)
    end = time.perf_counter() - start
    ## Y devuelve los resultados concatenados devueltos por las corrutinas y el tiempo que tardó en finalizar
    print(f"-->Encadenado result{n} => {segu} (tomó {end:0.2f} s).")

async def main(*args):

    ## Se guardan las corrutinas necesarias en el event loop de asyncio, que va a esperar que estas finalicen su ejecucion
    await asyncio.gather(*(chain(n) for n in args))
    # asyncio.gather( chain(n1), chain(n2), chain(n3), ...)
    # default: asyncio.gather( chain(1), chain(2), chain(3))

if __name__ == "__main__":
    import sys
    random.seed(414)

    args = [1, 2, 3] if len(sys.argv) == 1 else map(int, sys.argv[1:])
    start = time.perf_counter()
    
    ## asyncio.run se encarga de correr la función main a la que le pasamos una lista como argumento 
    asyncio.run(main(*args))
    end = time.perf_counter() - start

    ## imprime el tiempo total que tardó el programa en correr
    print(f"Program finished in {end:0.2f} seconds.")
