#1 - Escriba un programa que cree dos hilos utilizando el modulo concurrent.futures.
#  Cada uno mostrará por pantalla un mensaje y terminará. El programa luego de eso mostrará un 
# mensaje de finalización y retornará.

import concurrent.futures
import threading
import time

# con submit 
def saludar():
    print('hello, im thread ',threading.current_thread().name)
    time.sleep(.5)

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(saludar)
        future2 = executor.submit(saludar)

    if future1.done() and future2.done():
        print("la tarea se realizo con exito!")


