https://rico-schmidt.name/pymotw-3/asyncio/index.html

Mientras que el módulo threading implementa concurrencia a través de hilos de aplicación y multiprocessing implementa la concurrencia usando procesos del sistema, asyncio utiliza un enfoque de un solo hilo y un solo proceso en el que partes de una aplicación cooperan para cambiar tareas explícitamente en momentos óptimos.

async def = coroutine object que se puede ejecutar


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



$$$ sleep() always suspends the current task, allowing other tasks to run.
coroutine asyncio.sleep(delay, result=None)
-Block for delay seconds.
-If result is provided, it is returned to the caller when the coroutine completes.


Running Tasks Concurrently

$$$ awaitable asyncio.gather(*aws, return_exceptions=False)
-Run awaitable objects in the aws sequence concurrently.
-If any awaitable in aws is a coroutine, it is automatically scheduled as a Task. IMPORTANTE: no necesito crear las tasks
-If all awaitables are completed successfully, the result is an aggregate list of returned values. The order of result values corresponds to the order of awaitables in aws.