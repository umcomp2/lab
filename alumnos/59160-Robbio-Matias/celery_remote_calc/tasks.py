from celery import Celery

app = Celery('caluladora',broker='redis=://localhost',backend='redis=://localhost:6379',include=['calculadora'])

@app.task
def suma(a, b):
    return a+b

@app.task
def resta(a, b):
    return a-b

@app.task
def mult(a, b):
    return a*b

@app.task
def div(a, b):
    if b!=0:
        return a/b
    return 0

@app.task
def pot(x,y):
    return x**y

if __name__ == '__main__':
    app.start()