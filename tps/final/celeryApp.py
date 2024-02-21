from celery import Celery
from postgres import *
import psycopg2

#funcion reserva como tarea para ir almacenandola en la cola de tareas redis
# @app.task
# def nuevaReserva(horario, diaSemana, nombre, dni):
#     conexDB = conexionDB()
#     cursor = conexDB.cursor()
#     crear_tablas(conexDB)
#     try:
#         #insertar nombre del cliente
#         cursor.execute("INSERT INTO reservas (nombre) VALUES (%s)", (nombre,))
#         conexDB.commit()

#         #insertar dni del cliente

app = Celery('tasks', broker="redis://localhost:6379", backend="redis://localhost:6379")

# @app.task
# def getDiasSemana():
#     conexDB = conexionDB()
#     cursor = conexDB.cursor()

    
#     try:
#         cursor.execute("SELECT id, dia_semana FROM semana")
#         dias_semana = cursor.fetchall()
#         diasList = []
#         for d in dias_semana:
#             diaId, nombreDia = d
#             diasList.append({'id':diaId, 'dia_semana': nombreDia})
#         return diasList
    
#     except psycopg2.Error as e:
#         print("Error al obtener los días disponibles:", e)
#     finally:
#         if conexDB:
#             cursor.close()
#             conexDB.close()
        




