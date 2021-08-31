
from concurrent.futures import ThreadPoolExecutor


def tarea():
    return 'ejecutando tarea'

def main():

    with ThreadPoolExecutor(max_workers=2) as executor:
        t1 = executor.submit(tarea)
        t2 = executor.submit(tarea)
        print(t1.result())
        print(t2.result())


if __name__ == '__main__':
    main()
    print('Terminaron los hilos')