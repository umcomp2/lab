from celery import Celery
import math

# Definición de calculadora para Celery
app = Celery('crc_server', broker='redis://localhost',
             backend='redis://localhost:6379', include=['crc_server'])


@app.task
def suma(n, m):
    return n+m


@app.task
def resta(n, m):
    return n-m


@app.task
def mult(n, m):
    return n*m


@app.task
def div(n, m):
    if m != 0:
        return n/m
    return 0


@app.task
def pot(n, m):
    return n**m


@app.task
def sqrt(n):
    return math.sqrt(n)


@app.task
def fact(n):
    return math.factorial(n)


if __name__ == "__main__":
    app.start()
