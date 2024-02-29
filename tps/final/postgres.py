#conexion de base de datos

import psycopg2

def conexionDB():
    dbname= 'pilatesdb2'
    user = 'milicomputacion'
    password = '1234'
    host = 'localhost' 
    port = '5432' #puerto predeterminado

    try:
        dbConnection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        print("¡La conexion a la base de datos ha sido exitosa! ")
        return dbConnection
    except psycopg2.Error as e:
        print("Error en la conexion de la base de datos: ", e)
        return None
    
def crear_tablas(dbConnection):
    cursor = dbConnection.cursor()

    try:

        # Crear tabla Horarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS horarios (
                id SERIAL PRIMARY KEY,
                horario VARCHAR(10) UNIQUE
            )
        """)
        dbConnection.commit()
        print("¡Tabla horarios creada exitosamente!")

        #cursor.execute("INSERT INTO horarios (horario) VALUES ('9:00'), ('10:00'), ('15:00'), ('16:00'), ('19:00')")

        
        # Crear tabla Semana
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semana (
                id SERIAL PRIMARY KEY,
                dia_semana VARCHAR(20) UNIQUE
            )
        """)
        cursor.execute("INSERT INTO semana (dia_semana) VALUES ('lunes'), ('martes'), ('miércoles'), ('jueves'), ('viernes')")

        dbConnection.commit()
        print("¡Tabla Semana creada exitosamente!")

        # Crear tabla Cantidad
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cantidad (
                id SERIAL PRIMARY KEY,
                id_horario INTEGER REFERENCES horarios(id),
                id_dia_semana INTEGER REFERENCES semana(id),
                cantidad INTEGER
            )
        """)
        # Insertar datos en tabla cantidad
        # for horario_id in range(1, 6):
        #     for semana_id in range(1, 6):
        #         cursor.execute("INSERT INTO cantidad (id_horario, id_dia_semana, cantidad) VALUES (%s, %s, 0)", (horario_id, semana_id))

        dbConnection.commit()
        print("¡Tabla cantidad creada exitosamente!")
        # Crear tabla Reservas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id SERIAL PRIMARY KEY,
                id_horario INTEGER REFERENCES horarios(id),
                id_dia_semana INTEGER REFERENCES semana(id),
                dni VARCHAR(20),
                nombre VARCHAR(100)
            )
        """)

        dbConnection.commit()
        print("¡Tabla reservas creada exitosamente!")
    except psycopg2.Error as e:
        print("Error al crear tablas:", e)
        dbConnection.rollback() 

def getDias(dbConnection):
    cursor = dbConnection.cursor()
    try:
        cursor.execute("SELECT id, dia_semana FROM semana")
        diaSemana = cursor.fetchall()
        return diaSemana
    except:
        pass

def getHorarios(dbConnection):
    cursor = dbConnection.cursor()
    try:
        cursor.execute("SELECT id, horario FROM horarios")
        horario = cursor.fetchall()
        return horario
    except:
        pass

def getDisponibilidad(dbConnection, idDia, idHora):
    cursor = dbConnection.cursor()
    try:  
        cursor.execute("SELECT cantidad FROM cantidad WHERE id_horario = %s AND id_dia_semana= %s", (idHora, idDia))
        disponibilidad = cursor.fetchall()
        if disponibilidad:
            return disponibilidad[0]
        else:
            return None
    except Exception as e:
        print("Error al obtener la disponibilidad:", e)
        pass

def addCantidad(dbConnection, idDia, idHora):
    cursor = dbConnection.cursor()
    try:  
        cursor.execute("SELECT cantidad FROM cantidad WHERE id_horario = %s AND id_dia_semana= %s", (idHora, idDia))
        disponibilidad = cursor.fetchall()

        for i in enumerate(disponibilidad[0]):
            cantidad = int(i[1])
            nuevaCantidad = cantidad + 1
            cursor.execute("UPDATE cantidad SET cantidad = %s WHERE id_horario = %s AND id_dia_semana = %s", (nuevaCantidad, idHora, idDia))
            dbConnection.commit()
            return nuevaCantidad
 
    except Exception as e:
        print("Error al disminuir la disponibilidad:", e)
        pass

def eliminarCantidad(dbConnection, idReserva):
    cursor = dbConnection.cursor()
    try:  
        cursor.execute("SELECT id_horario, id_dia_semana FROM reservas WHERE id = %s", (idReserva,))
        reservaId= cursor.fetchone()
        idHora, idDia = reservaId
        cursor.execute("SELECT cantidad FROM cantidad WHERE id_horario = %s AND id_dia_semana= %s", (idHora, idDia))
        disponibilidad = cursor.fetchall()

        for i in enumerate(disponibilidad[0]):
            cantidad = int(i[1])
            nuevaCantidad = cantidad - 1
            cursor.execute("UPDATE cantidad SET cantidad = %s WHERE id_horario = %s AND id_dia_semana = %s", (nuevaCantidad, idHora, idDia))
            dbConnection.commit()
            print("aumento de disponibilidad")
            return nuevaCantidad
 
    except Exception as e:
        print("Error al aumentar la disponibilidad:", e)
        pass

def dniExiste(dbConnection, dni):
    validate=True
    try:    
        cursor = dbConnection.cursor()
        cursor.execute("SELECT * FROM reservas WHERE dni = %s", (dni,))
        reservas = cursor.fetchall()
        if len(reservas) > 0:
            print("Se encontraron reservas con el DNI especificado.")
            for reserva in reservas:
                print(reserva) 
            return validate     
                 # Puedes personalizar cómo quieres mostrar los datos de la reserva
        else:
            print("No se encontraron reservas con el DNI especificado.")
            validate = False
            return validate
        
    except Exception as error:
        print("Error al conectar a la base de datos PostgreSQL:", error)

def getReservasDni (dbConnection, dni):
    reservas = []
    try:    
        cursor = dbConnection.cursor()
        cursor.execute("""
                SELECT reservas.id,
                (SELECT horario FROM horarios WHERE id = reservas.id_horario) AS nombre_horario,
                (SELECT dia_semana FROM semana WHERE id = reservas.id_dia_semana) AS nombre_dia_semana,
                reservas.dni,
                reservas.nombre
            FROM reservas
            WHERE reservas.dni = %s
        """, (dni,))
        turno = cursor.fetchall()
        for i in turno:

            reservas.append(i)
        
        return reservas

    
    except Exception as e:
        print("Error al obtener las reservas:", e)
        pass

def addHorario(dbConnection, hora):
    try:
        cursor = dbConnection.cursor()
        cursor.execute("INSERT INTO horarios (horario) VALUES (%s)", (hora,))
        dbConnection.commit()
        print("Horario agregado correctamente")
    except Exception as e:
        print("Error al obtener las reservas:", e)
        pass

def addDia(dbConnection, dia):
    try:
        cursor = dbConnection.cursor()
        cursor.execute("INSERT INTO semana (dia_semana) VALUES (%s)", (dia,))
        dbConnection.commit()
        print("Horario agregado correctamente")
    except Exception as e:
        print("Error al obtener las reservas:", e)
        pass  

def addHoraInCantidad(dbConnection, hora):
    try:
        cursor = dbConnection.cursor()
        cursor.execute("SELECT id FROM semana")  
        idSemana = cursor.fetchall()
        print(idSemana)
        
        cursor.execute("SELECT id FROM horarios WHERE horario=%s",(hora,)) 
        idHorario = cursor.fetchall()
        print(idHorario)
        for d in idSemana:
                cursor.execute("SELECT COUNT(*) FROM cantidad WHERE id_horario=%s AND id_dia_semana=%s", (idHorario[0], d[0]))
                existencia = cursor.fetchone()[0]
                if existencia == 0:
                        cursor.execute("INSERT INTO cantidad (id_horario, id_dia_semana, cantidad) VALUES (%s, %s, 0)", (idHorario[0], d[0]))
        dbConnection.commit()
        print("Relaciones de horarios y días de la semana agregadas exitosamente.")
       
    except Exception as e:
        print("Error al relacionar horario y dia:", e)


def deleteHoraInCantidad(dbConnection, idHora):
    try:
        cursor = dbConnection.cursor()
        cursor.execute("DELETE FROM cantidad WHERE id_horario=%s",(idHora,))
        dbConnection.commit()
        print("horario eliminado de la tabla cantidad")
        cursor.execute("DELETE FROM horarios WHERE id=%s", (idHora,))
        dbConnection.commit()
        print("horario eliminado de la tabla horarios")


    except Exception as e:
        print("Error al eliminar el horario: ", str(e))
    finally:
        cursor.close()
        dbConnection.close()
