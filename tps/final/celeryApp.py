from celery import Celery
from celeryConfiguration import *
from postgres import *
import psycopg2

#funcion reserva como tarea para ir almacenandola en la cola de tareas redis