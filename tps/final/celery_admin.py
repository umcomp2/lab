from celery import Celery
from celery_config import app
from postgresql import connect_to_db;
import psycopg2

@app.task
def agregar_evento(nombre_evento, sectores):
    connection_db = connect_to_db()
    if connection_db:
        try:
            # Obtengo un cursor para ejecutar consultas SQL
            cursor = connection_db.cursor()

            # Inserto el evento en la tabla de eventos
            cursor.execute("INSERT INTO eventos (nombre_evento) VALUES (%s) RETURNING id", (nombre_evento,))
            evento_id = cursor.fetchone()[0]

            # Inserto los sectores del evento en la tabla de sectores
            for sector, capacidad in sectores.items():
                cursor.execute("INSERT INTO sectores (evento_id, nombre_sector, capacidad) VALUES (%s, %s, %s)",
                               (evento_id, sector, capacidad))

            # Confirmo los cambios en la base de datos
            connection_db.commit()
            print("Evento agregado exitosamente.")

        except psycopg2.Error as e:
            print("Error al agregar evento a la base de datos:", e)

        finally:
            if connection_db:
                cursor.close()
                connection_db.close()


@app.task
def suma(n, m):
    return n+m

