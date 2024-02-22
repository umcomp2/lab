from celery import Celery
from postgres import *
import psycopg2

app = Celery('tasks', broker="redis://localhost:6379", backend="redis://localhost:6379")

@app.task
def nuevaReserva(id_horario, id_dia_semana, dni, nombre):
    dbConnection = conexionDB()
    cursor = dbConnection.cursor()
    try:
        #traer Dia Semana
        cursor.execute("SELECT dia_semana FROM semana WHERE id = %s", (id_dia_semana,))
        diaElegido = cursor.fetchall()
        #traer horario
        cursor.execute("SELECT horario FROM horarios WHERE id = %s", (id_horario,))
        horarioElegido = cursor.fetchall()
        #agregar datos a la tabla reserva
        cursor.execute("INSERT INTO reservas (id_horario, id_dia_semana, dni, nombre) VALUES (%s, %s, %s,%s)",
                       (id_horario, id_dia_semana, dni, nombre))
        dbConnection.commit()
        print("reserva realizada con exito")
    except Exception as e:
        print("Error al hacer la reserva: ", str(e))
    finally:
        cursor.close()
        dbConnection.close()

@app.task
def cancelarTurno(id_reserva):
    dbConnection = conexionDB()
    cursor = dbConnection.cursor()
    try:
        
        cursor.execute("DELETE FROM reservas WHERE id=%s",( id_reserva,))
        dbConnection.commit()
        
        
    except Exception as e:
        print("Error al hacer la cancelar el turno: ", str(e))
    finally:
        cursor.close()
        dbConnection.close()

   




