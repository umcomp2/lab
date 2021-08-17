from listas import *
from common import *
from concurrent.futures import *


def llenar_matriz(i):
    pass



def main():
    
    rlist, glist, blist = processList()
    print(len(rlist), len(glist), len(blist))

    '''with ThreadPoolExecutor(max_workers=3) as executor:
        
        executor.map(llenar_matriz, rlist)
        executor.map(llenar_matriz, glist)
        executor.map(llenar_matriz, blist)
    '''

if __name__ == "__main__":
    main()