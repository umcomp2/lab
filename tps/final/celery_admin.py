from celery import Celery
from celery_config import app
from postgresql_config import *
import psycopg2

@app.task
def new_event(nombre_evento, sectores):
    connection_db = connect_to_db()
    cursor = connection_db.cursor()
    create_eventos_table(connection_db)

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
        cursor.close()
        connection_db.close()


@app.task
def get_events():
    connection_db = connect_to_db()
    cursor = connection_db.cursor()

    try:
        cursor.execute("SELECT id, nombre FROM eventos")
        eventos = cursor.fetchall()

        # Armo una lista de diccionarios con los eventos y sus detalles
        eventos_list = []
        for evento in eventos:
            evento_id, nombre_evento = evento
            cursor.execute("SELECT nombre, capacidad FROM sectores WHERE evento_id = %s", (evento_id,))
            sectores = cursor.fetchall()
            sectores_dict = [{'nombre': sector[0], 'capacidad': sector[1]} for sector in sectores]

            eventos_list.append({'id': evento_id, 'nombre': nombre_evento, 'sectores': sectores_dict})

        print("Eventos recuperados con éxito")
        return eventos_list

    except Exception as e:
        print("Error al recuperar los eventos:", e)

    finally:
        cursor.close()
        connection_db.close()

@app.task
def get_sectores(evento_id):
    connection_db = connect_to_db()
    cursor = connection_db.cursor()

    try:
        # Consultar los sectores del evento en la tabla de sectores
        cursor.execute("SELECT nombre, capacidad FROM sectores WHERE evento_id = %s", (evento_id,))
        sectores = cursor.fetchall()
        sectores_list = [{'nombre': sector[0], 'capacidad': sector[1]} for sector in sectores]

        print(f"Sectores del evento {evento_id} recuperados con éxito")
        return sectores_list

    except Exception as e:
        print(f"Error al recuperar los sectores del evento {evento_id}:", e)

    finally:
        # Cerrar la conexión con la base de datos
        cursor.close()
        connection_db.close()