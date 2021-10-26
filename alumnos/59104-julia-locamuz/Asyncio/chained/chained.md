Para poder explicar 'chained.py' primero hay que explicar 3 conceptos muy importantes del modulo asyncio,
dando por hecho que se conoce la funcionalidad del mismo: 
    'asyncio is a library to write concurrent code using the async/await syntax'

There are three main types of awaitable objects: coroutines, Tasks, and Futures.

*Coroutines

Python coroutines are awaitables and therefore can be awaited from other coroutines
a coroutine function: an async def function;

*Tasks

Tasks are used to schedule coroutines concurrently.
When a coroutine is wrapped into a Task with functions like asyncio.create_task() the coroutine is automatically scheduled to run soon

*Futures

A Future is a special low-level awaitable object that represents an eventual result of an asynchronous operation.
When a Future object is awaited it means that the coroutine will wait until the Future is resolved in some other place.

Teniendo estos conceptos claros, se puede ver en el script que hay 4 couroutines, siendo main()  'the top-level entry point “main()” function' 
Las otras tres son 'primera', 'segunda' y 'chained'

EXPLICACION DEL CODIGO chained.py

En primer lugar se ejecuta el bloque de se encuentra en 'if __name__ = '__main__'':
    1) random.seed(414) 
        La función semilla (seed) se usa para guardar el estado de una función aleatoria, de modo que pueda generar los mismos números aleatorios en múltiples ejecuciones del código en la misma máquina o en diferentes máquinas (para un valor semilla específico)
    2) Se importa el modulo sys y se hace uso de sys.argv (lista de argumentos de la línea de comandos pasados a un script de Python. argv[0] es el nombre del script ) 
        si no se le pasa argumentos al script (es decir si len(argv) == 1) se toma como parametros una lista dada, 
        si no se toman esos argumentos proporcionados por el usuario convirtiendolos en int con un mapeo 
    3) se inicia un contador 
    4) se utiliza asyncio.run(main()) para correr la funcion principal (top-level entry point “main()” function) 
        proporcionandole una lista de argumentos

Al ejecutarse la funcion main() se ejecuta un ' awaitable asyncio.gather ' , lo que hace es programar tres llamadas al mismo tiempo, es decir ejecutar los 'awaitable objects' en la secuencia de los args pasados como parametro al mismo tiempo (If any awaitable in aws is a coroutine, it is automatically scheduled as a Task)
En este caso se llama n veces a la corrutina chain(n) dependiendo de cuantos parametros le pase al programa, por defecto 3 veces, y se las envuelve en tasks.

Por cada llamada a chain:
    - se inicia 'cronometro'
    - se llama mediante un await a la corutina 'primera' pasandole como parametro n (prim = await primera(n))
        - dentro de primera se ejecuta un await asyncio.sleep(i) siendo i  un numero random del 0 al 9 
        -->  Pausará la tarea actual y permitirá que se ejecuten otras tasks
            Esta función toma un solo parámetro que es un número de segundos, y devuelve un **futuro** que aún no está marcado como hecho, pero que será cuando haya pasado el número especificado de segundos. 

            Al usar asyncio.sleep con un parámetro distinto de cero, vale la pena señalar que el hecho de que el futuro se haga cuando haya pasado el número de segundos no significa que su tarea siempre se reactivará en ese momento. De hecho, puede volver a activarse en cualquier momento después de ese tiempo, ya que solo puede activarse cuando no se está ejecutando ninguna otra tarea en el bucle de eventos.

            The distinction between a Coroutine and a Future is important. A Coroutine’s code will not be executed until it is awaited. A future represents something that is executing anyway, and simply allows your code to wait for it to finish, check if it has finished, and fetch the result if it has.

    - al haberse devuelto un valor en la funcion, es decir al haber finalizado la misma, se ejecuta corrutina segunda (segu = await segunda(n, prim)) pasandole como parametro prim (objeto futuro)

Estas llamadas se van ejecutando de manera concurrente, el orden se basa en su parametro i, la de menor i sera la primera en pasar a la corrutina 'primera' y 'segunda'. Cada chain debe completar la corrutina 'primera' para pasar a la 'segunda' (por eso el nombre del programa chained.py) pero las distintas llamadas a chain son asincronas. Pueden terminar en cualquier orden (depende del numero random)