from celery import Celery
from celery_config import app
from postgresql import connect_to_db;
import psycopg2

@app.task
def new_event(nombre_evento, sectores):
    connection_db = connect_to_db()
    cursor = connection_db.cursor()

    try:
        # Insertar el evento en la tabla de eventos
        cursor.execute("INSERT INTO eventos (nombre) VALUES (%s)", (nombre_evento,))
        connection_db.commit()

        # Obtener el ID del evento recién insertado
        cursor.execute("SELECT lastval()")
        evento_id = cursor.fetchone()[0]

        # Insertar los sectores del evento en la tabla de sectores
        for sector in sectores:
            cursor.execute("INSERT INTO sectores (evento_id, nombre, capacidad) VALUES (%s, %s, %s)",
                           (evento_id, sector['nombre'], sector['capacidad']))
        connection_db.commit()

        print("Evento agregado con éxito")

    except Exception as e:
        print("Error al agregar el evento:", e)
        connection_db.rollback()

    finally:
        # Cerrar la conexión con la base de datos
        cursor.close()
        connection_db.close()


@app.task
def suma(n, m):
    return n+m

