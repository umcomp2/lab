from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


values = [1, 2]

def task(n):
    return 'ejecutando hilo {}'.format(n)

def main():
   with ThreadPoolExecutor(max_workers = 2) as executor:
      results = executor.map(task, values)
   for result in results:
      print(result)


if __name__ == '__main__':
   main()
