#conexion de base de datos

import psycopg2

def conexionDB():
    dbname= 'pilatesDB'
    user = 'postgres'
    password = 'admin'
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
    try:
        cursor = dbConnection.cursor()

        # Crear tabla Horarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS horarios (
                id SERIAL PRIMARY KEY,
                horario VARCHAR(10) UNIQUE
            )
        """)
        cursor.execute("INSERT INTO horario (horario) VALUES ('9:00'), ('10:00'), ('15:00'), ('16:00'), ('19:00')")


        # Crear tabla Semana
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semana (
                id SERIAL PRIMARY KEY,
                dia_semana VARCHAR(20) UNIQUE
            )
        """)
        cursor.execute("INSERT INTO semana (dia_semana) VALUES ('lunes'), ('martes'), ('miércoles'), ('jueves'), ('viernes')")


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
        for horario_id in range(1, 6):
            for semana_id in range(1, 6):
                cursor.execute("INSERT INTO cantidad (id_horario, id_semana, cantidad) VALUES (%s, %s, 0)", (horario_id, semana_id))


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
        print("¡Tablas creadas exitosamente!")
    except psycopg2.Error as e:
        print("Error al crear tablas:", e)
        dbConnection.rollback() 

def crear_reserva(dbConnection, id_horario, id_dia_semana, dni, nombre):
    try:
        cursor = dbConnection.cursor()
        
        # Verificar si la cantidad de reservas excede el límite de 15 personas
        cursor.execute("SELECT cantidad FROM cantidad WHERE id_horario = %s AND id_dia_semana = %s", (id_horario, id_dia_semana))
        cantidad_actual = cursor.fetchone()[0]
        if cantidad_actual >= 15:
            print("No se puede hacer la reserva. Se ha alcanzado el límite de 15 personas.")
            return

        # Insertar reserva
        cursor.execute("INSERT INTO reservas (id_horario, id_dia_semana, dni, nombre) VALUES (%s, %s, %s, %s)", (id_horario, id_dia_semana, dni, nombre))
        dbConnection.commit()
        print("Reserva creada exitosamente!")
    except psycopg2.Error as e:
        print("Error al crear reserva:", e)
        dbConnection.rollback()
    finally: 
        cursor.close()
