from celery import Celery
from time import sleep

app = Celery('tasks', broker='redis://localhost', backend='db+sqlite:///db.sqlite3')

@app.task
def add(x, y):
    sleep(5)
    return x + y