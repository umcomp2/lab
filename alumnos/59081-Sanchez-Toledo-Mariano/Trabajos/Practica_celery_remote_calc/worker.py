from celery import Celery


appCele = Celery('tasks', broker='redis://localhost', backend='redis://localhost:6379')

@appCele.task
def suma(num1, num2):
    print('suma')
    return str(num1+num2)

@appCele.task
def resta(num1, num2):
    return str(num1-num2)

@appCele.task
def multiplicar(num1, num2):
    return str(num1*num2)

@appCele.task
def dividir(num1, num2):
    return str(num1/num2)