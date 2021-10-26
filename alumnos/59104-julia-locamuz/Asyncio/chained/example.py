import asyncio

async def fetch_data():
    print('start fetching')
    # sleep() always suspends the current task, allowing other tasks to run.
    await asyncio.sleep(2) # otorga procesamiento a otra task de la pila --> print_numbers
    print('done fetching') # dsps de dormir 2 segundos y darle procesamiento a print_numbers (le alcanzo para imprimir 4 digitos)
    return {'data': 1} # finaliza --> control a otra task de la pila

async def print_numbers():
    print('start printing') # tengo 2 segundos 
    for i in range(10):
        print(i)
        await asyncio.sleep(0.5) # con mis 2 segundos puedo imprimir 4 numeros --> sigue fetch_data --> finaliza --> sigo imprimiendo

async def main():
    # The asyncio.create_task() function to run coroutines concurrently as asyncio Tasks.
    
    # When a coroutine is wrapped into a Task with functions like asyncio.create_task()
    # the coroutine is automatically scheduled to run soon
    task2 = asyncio.create_task(print_numbers())  # crea task pero no la corre hasta que no se realiza await 
 
    # en mi "pila de tasks" tengo 2 tasks...
    await fetch_data() # corre fetch data
    await task2


# event loop to run the program 
# The asyncio.run() function to run the top-level entry point “main()” function
asyncio.run(main())

'''
start fetching
start printing
0
1
2
3
done fetching
4
5
6
7
8
9
'''