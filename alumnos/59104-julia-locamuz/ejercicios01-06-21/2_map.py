from concurrent.futures import ThreadPoolExecutor
import time 

monto = 0 

def depositar(deposito): 
    global monto
    print('depositando {} de monto ({})...'. format(deposito, monto))
    monto += deposito

def extraer(extraccion): 
    global monto
    print('extrayendo {} de monto ({})...'. format(extraccion, monto))
    monto -= extraccion

if __name__ == '__main__':
    depositos = [10, 20, 30, 40]
    extracciones = [20,10]
    ex = ThreadPoolExecutor(max_workers=2)
    ex.map(depositar, depositos)
    time.sleep(.2)
    extraccion = ex.map(extraer, extracciones)
    time.sleep(.5)
    print('monto final: ', monto)