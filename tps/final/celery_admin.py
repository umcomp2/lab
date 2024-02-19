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
        cursor.close()
        connection_db.close()

@app.task
def comprar_entradas(evento_id, sector_nombre, cantidad_entradas, dni_comprador):
    connection_db = connect_to_db()
    cursor = connection_db.cursor()
    create_compra_table(connection_db)

    try:
        cursor.execute("SELECT nombre FROM eventos WHERE id = %s", (evento_id))
        evento_nombre = cursor.fetchone()[0]
         # Traigo el id del sector
        cursor.execute("SELECT id FROM sectores WHERE evento_id = %s AND nombre = %s", (evento_id, sector_nombre))
        sector_id = cursor.fetchone()[0]
        if sector_id is None:
            print("El sector especificado no existe.")
            return "El sector especificado no existe."

        # Query para hacer la compra
        cursor.execute("INSERT INTO Compra (dni_comprador, evento_id, sector_id, cantidad_entradas) VALUES (%s, %s, %s, %s)",
                       (dni_comprador, evento_id, sector_id, cantidad_entradas))
        connection_db.commit()

        # Verificar disponibilidad
        cursor.execute("SELECT capacidad FROM sectores WHERE evento_id = %s AND nombre = %s", (evento_id, sector_nombre))
        capacidad_sector = cursor.fetchone()[0]
        if capacidad_sector is None:
                print("No se encontró información sobre la capacidad de este sector.")
                return "No se encontró información sobre la capacidad de este sector."
        
        if cantidad_entradas > capacidad_sector:
            print("No hay suficientes entradas disponibles en este sector.")
            return "No hay suficientes entradas disponibles en este sector."

        # Actualizo cantidad
        cursor.execute("UPDATE sectores SET capacidad = capacidad - %s WHERE evento_id = %s AND nombre = %s",
                       (cantidad_entradas, evento_id, sector_nombre))
        connection_db.commit()

        print(f"{cantidad_entradas} entradas compradas con éxito en el sector {sector_nombre} del evento {evento_nombre}.")
        return f"{cantidad_entradas} entradas compradas con éxito en el sector {sector_nombre} del evento {evento_nombre}."

    except Exception as e:
        print("Error al comprar entradas:", e)
        connection_db.rollback()
        return "Error al comprar entradas. Por favor, inténtelo de nuevo."

    finally:
        cursor.close()
        connection_db.close()

@app.task
def buscar_compras_por_dni(dni_comprador,eventos):
    connection_db = connect_to_db()
    cursor = connection_db.cursor()

    try:
        compras_por_dni = {}

        for evento in eventos:
            evento_id = evento['id']
            evento_nombre = evento['nombre']

            # Consultar las compras realizadas por el comprador en el evento actual
            cursor.execute("SELECT * FROM Compra WHERE dni_comprador = %s AND evento_id = %s", (dni_comprador, evento_id))
            compras = cursor.fetchall()

            if compras:
                compras_por_dni[evento_nombre] = compras

        if compras_por_dni:
            print(f"Compras encontradas para el DNI {dni_comprador}:")
            return compras_por_dni
        else:
            print(f"No se encontraron compras para el DNI {dni_comprador}.")
            return f"No se encontraron compras para el DNI {dni_comprador}."

    except Exception as e:
        print("Error al buscar compras por DNI:", e)
        return None

    finally:
        cursor.close()
        connection_db.close()

