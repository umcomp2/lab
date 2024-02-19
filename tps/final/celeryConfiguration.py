from celery import Celery
from postgres import *

app = Celery('tasks', broker="redis://localhost:6379", backend="redis://localhost:6379", include = ['celeryApp'])

#nombre de la aplicacion celery: tasks
#broker="redis://localhost:6379" -->  url del broker que celery usa para comunicarse
#backend="redis://localhost:6379" --> url donde celry va a almacenar los resultados de las tareas
#include = ['celery'] --> modulo que se importara al iniciar la app celery
#en este caso redis funciona como brocker y backend