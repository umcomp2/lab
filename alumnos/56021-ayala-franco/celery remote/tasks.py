from celery import Celery

app = Celery('tasks', backend='redis://localhost:6379', broker='redis://localhost:6379')

@app.task
def add(x, y):
    return x + y

@app.task
def subtract(x, y):
    return x - y

@app.task
def multiply(x, y):
    return x * y

@app.task
def divide(x, y):
    return x / y

@app.task
def power(x, y):
    return x**y