import psycopg2

def connect_to_db():
    dbname = 'ticketsdb'
    user = 'postgres'
    password = 'admin'
    host = 'localhost' 
    port = '5432'       

    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        print("Conexión exitosa a la base de datos.")
        return connection
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None



def create_eventos_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL
            )
        """)
        connection.commit()
        print("Tabla 'eventos' creada exitosamente.")

        # Crear la tabla 'sectores'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sectores (
                id SERIAL PRIMARY KEY,
                evento_id INT REFERENCES eventos(id),
                nombre VARCHAR(255) NOT NULL,
                capacidad INT
            )
        """)
        connection.commit()
        print("Tabla 'sectores' creada exitosamente.")

    except psycopg2.Error as e:
        print("Error al crear la tabla 'eventos' o 'sectores':", e)

# if __name__ == "__main__":
#     connect_to_db()