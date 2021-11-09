from calc_config import app

"""
Funciones matematicas
"""

@app.task
def suma(x : float, y : float) -> float:
    return x + y

@app.task
def resta(x : float, y : float) -> float:
    return x - y

@app.task
def mult(x : float, y : float) -> float:
    return x * y

@app.task
def div(x : float, y : float) -> float:
    return x / y

@app.task
def pot(x : float, y : float) -> float:
    return x ** y
