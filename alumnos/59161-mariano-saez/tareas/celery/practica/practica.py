from celery import Celery

app = Celery("practica", broker="redis://localhost", backend="redis://localhost:6379")

@app.task
def add(x : int, y : int):
    return x + y

@app.task
def summation(x : list):
    return sum(x)

if __name__ == "__main__":
    app.start()