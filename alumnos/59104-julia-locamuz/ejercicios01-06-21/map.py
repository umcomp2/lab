import concurrent.futures
import threading
import time

numeros = [1,2,3,4,5,6]

def doblar(n):
    return n**2

if __name__ == '__main__':
    ex = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    results = ex.map(doblar, numeros)

    for i in results: 
        print(i)