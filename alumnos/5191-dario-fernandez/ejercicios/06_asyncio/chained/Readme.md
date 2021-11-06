Uso
    
    python3 chained.py
    python3 chained.py 4 5 8 9

Se ejecuta primero la funcion: 
### __name__ == "__main__"
    random.seed(417)
Es un metodo para inicializar los numeros pseudoaleatorios a partir de una semilla

    args = [1, 2, 3] if len(sys.argv) == 1 else list(map(int, sys.argv[1:]))
Crea una lista de numeros enteros por defecto args es [1,2,3]
Se puede pasar como argumento otros valores mediante linea de comando

    asyncio.run(main(*args))  
    
Se encarga de ejecutar la funcion main pasandole como argumento la variable args

###async def main(*args):
    Inicializa cronómetro
    await asyncio.gather(*(chain(n) for n in args))
    Finaliza el cronómetro e imprime como resultado la cantidad de tiempo que tardo en ejecutarse las tareas 

Se pasa a ejecutar objetos esperables de forma concurrente, llamando a la funcion chain n veces dependiendo la cantidad
de elementos que tenga la lista que recibe como paramétro "args"

###async def chain(n: int) -> None:
    Es una co-rutina la cual espera como argumento un valor entero y no retorna nada
    Inicializa un cronómetro
    Se llama a la función primera pasandole como parametro un valor entero y se queda esperandola, luego llama
    a la función segunda mandandole como argumento el valor entero y el resultado del metodo "primera"
    Finaliza el cronómetro e imprime como resultado la cantidad de tiempo que tardo en ejecutarse ambas tareas
    
###async def primera(n: int) -> str:
    
Es una co-rutina la cual espera como argumento un valor entero y retorna un string
    
    i = random.randint(0, 10)
Se genera un valor random del 0 al 9

    await asyncio.sleep(i)
Pausa la tarea n segundos, permitiendo que se ejecuten otras y devuelve un objeto futuro

###async def segunda(n: int, arg: str) -> str:

Es una co-rutina la cual espera como argumento un valor entero y el valor devuelto del método "primera" y retorna un string
    
    i = random.randint(0, 10)
Se genera un valor random del 0 al 9
    
    await asyncio.sleep(i)
Pausa la tarea n segundos, permitiendo que se ejecuten otras y devuelve un objeto futuro
