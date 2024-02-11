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

