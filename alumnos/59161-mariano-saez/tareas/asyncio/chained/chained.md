import asyncio
import random
import time


# Funcion asincrona - primera(n) : str
    # Recibe un parametro n : int el cual se utilizara en la devolucion
    # del str f"result {n} - A", luego de un tiempo aleatorio entre 0 y 10
async def primera(n: int) -> str:
    i = random.randint(0, 10)
    print(f"primera({n}) esperando {i}s.")

    # Se le devuelve el control al event loop de esta forma
    # se pueden ejecutar todos las otra chain() dentro del loop
    await asyncio.sleep(i)

    print(f"Retornando primera({n}) == {result}.")
    return f"result{n} - A"


# Funcion asincrona - segunda(n, arg) : str
    # Recibe un parametro n : int y otro arg : str el cual se utilizara en 
    # la devolucion del str f"result {n} - A", luego de un tiempo
    # aleatorio entre 0 y 10
async def segunda(n: int, arg: str) -> str:
    i = random.randint(0, 10)
    print(f"segunda{n, arg} esperando {i}s.")

    # Se le devuelve el control al event loop de esta forma
    # se pueden ejecutar todos las otras chain() dentro del loop
    await asyncio.sleep(i)
    
    print(f"Retornando segunda{n, arg} => {result}.")
    return f"result{n} - B => {arg}"


async def chain(n: int) -> None:
    start = time.perf_counter()
    print("\nLanzando primera")

    # Esta funcion contiene llamados a funciones que devuelven
    # el control al loop
    prim = await primera(n)
    print("\nLanzando Segunda")

    # Esta funcion contiene llamados a funciones que devuelven
    # el control al loop
    segu = await segunda(n, prim)

    end = time.perf_counter() - start

    # Muestra el resultado de la concateniacion de los resultados retornados
    # por las dos funciones y el tiempo de ejecucion
    print(f"\n\t--> Encadenado result{n} => {segu} (tomó {end:0.2f} s).")


async def main(*args):
    # " (chain(n) for n in args) "
    # Genera una tupla con llamados a funciones chain()
    # y a cada una le pasa uno de los argumentos entregados
    # por CLI o por defecto

    # Con gather se agregan las corutinas al event loop
    # y se espera a que todas finalicen

    # Con await evitamos que la funcion asicronica retorne
    # (haga yield) antes de que retorne gather con la tupla
    await asyncio.gather(*(chain(n) for n in args))
    
    # asyncio.gather( chain(n1), chain(n2), chain(n3), ...)
    # default: asyncio.gather( chain(1), chain(2), chain(3))

if __name__ == "__main__":
    import sys

    # Semilla para la generacion de numeros pseudoaleatorios
    random.seed(414)

    # Si no se proveen argumentos por CLI los argumentos por
    # defecto son 1, 2 y 3
    args = [1, 2, 3] if len(sys.argv) == 1 else map(int, sys.argv[1:])

    # Se incializa el Event loop con la funcion main() y los
    # argumentos pasados por CLI o por defecto
    asyncio.run(main(*args))
