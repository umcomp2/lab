from celery import Celery
from config import app

@app.task
def suma(x, y):
    return x+y

@app.task
def resta(x, y):
    return x-y

@app.task
def multiplicacion(x, y):
    return x*y

@app.task
def division(x, y):
    if y != 0:
        return x/y
    return 0

@app.task
def potencia(x, y):
    return x**y