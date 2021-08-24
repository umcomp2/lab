import concurrent.futures
import time 

total = 0
def depositar(saldo):
    depositado = int(input("Ingrese el saldo a depositar: "))
    saldo_actual = saldo + depositado

    print("Hilo 1 depositando {} -----> {}".format(depositado,saldo_actual))
    time.sleep(1)
    print("Su saldo actual es: ", saldo_actual)

def extraer(cola):
    extraer = int(input("Cuanto dinero quiere retirar:"))

    saldo_actual = total - extraer
    print("Hilo 2 extrayendo {} -----> {}".format(extraer, saldo_actual))
    time.sleep(1)
    print("Su saldo actual es:", saldo_actual)