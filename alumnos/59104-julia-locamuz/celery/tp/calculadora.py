
from celery_config import app

@app.task
def suma(n, m):
    return n + m

@app.task
def resta(n, m):
    return n - m

@app.task
def mult(n, m):
    return n * m

@app.task
def div(n, m):
    return n / m

@app.task
def pot(n, m):
    return n ** m


