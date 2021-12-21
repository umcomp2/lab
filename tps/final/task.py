from celery import Celery


app = Celery('tasks', broker="redis://localhost:6379", backend="redis://localhost:6379")


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
    return n/m

@app.task

def pot(n, m):
    return n**m
