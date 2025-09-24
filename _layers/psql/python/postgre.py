import psycopg2

POSTGRE_DB_HOST = "rdcmanager.claoesjfa0zq.us-east-1.rds.amazonaws.com"
POSTGRE_DB_PORT = "5432"
POSTGRE_DB_NAME = "postgres"
POSTGRE_DB_USER = "rdcom_admin"
POSTGRE_DB_PASS = "ceLItSDJmlazZV8E7aQ"

DB_HOST = "rdcmanager.claoesjfa0zq.us-east-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "rdcom_admin"
DB_PASS = "sceLItSDJmlazZV8E7aQ"

def query_postgresql(query):
    try:
        connection_params = {
            'dbname': POSTGRE_DB_NAME,
            'user': POSTGRE_DB_USER,
            'password': POSTGRE_DB_PASS,
            'host': POSTGRE_DB_HOST,
            'port': POSTGRE_DB_PORT
        }
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    
def insert_postgresql(query):
    try:
        connection_params = {
            'dbname': POSTGRE_DB_NAME,
            'user': POSTGRE_DB_USER,
            'password': POSTGRE_DB_PASS,
            'host': POSTGRE_DB_HOST,
            'port': POSTGRE_DB_PORT
        }
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute(query)

        inserted_id = 0
        
        # Si la consulta incluye un INSERT, obtenemos el id generado
        if "INSERT" in query.upper() and "RETURNING" in query.upper():
            inserted_id = cursor.fetchone()[0]  # Obtenemos el primer valor retornado (el id)
            
        if "UPDATE" in query.upper() and "RETURNING" in query.upper():
            inserted_id = cursor.fetchone()[0]  # Obtenemos el primer valor retornado (el id)

        conn.commit()  # Confirma la transacción

        cursor.close()
        conn.close()

        if inserted_id > 0:
            return inserted_id
        else:
            return True
    
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    
def insert_withoutId(query):
    try:
        connection_params = {
            'dbname': POSTGRE_DB_NAME,
            'user': POSTGRE_DB_USER,
            'password': POSTGRE_DB_PASS,
            'host': POSTGRE_DB_HOST,
            'port': POSTGRE_DB_PORT
        }
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute(query)

        conn.commit()  # Confirma la transacción

        cursor.close()
        conn.close()

        return True
    
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None    

def transaction_postgresql(queries):
    try:
        connection_params = {
            'dbname': POSTGRE_DB_NAME,
            'user': POSTGRE_DB_USER,
            'password': POSTGRE_DB_PASS,
            'host': POSTGRE_DB_HOST,
            'port': POSTGRE_DB_PORT
        }
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        conn.autocommit = False  # Desactiva el autocommit para la transacción

        for query in queries:
            cursor.execute(query)  # Aquí se corrige "excecute"

        conn.commit()  # Hace commit de la transacción si todo está bien
        return True

    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()  # Revertir cambios si ocurre un error
        print(f"Error: {error}")
        return False

    finally:
        if cursor:
            cursor.close()  # Cierra el cursor
        if conn:
            conn.close()  # Cierra la conexión
            
def db_read(query, user = "no_user", params=None):
    try:
        connection_params = {
            'dbname': DB_NAME,
            'user': DB_USER,
            'password': DB_PASS,
            'host': DB_HOST,
            'port': DB_PORT
        }
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute('SET session "my.app_user" = %s;', (user,))
        cursor.execute(query, params)  # Usamos parámetros

        results = cursor.fetchall()

        cursor.close()
        conn.close()
        return results

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None

def db_insert(query, user = "no_user", params=None):
    try:
        connection_params = {
            'dbname': DB_NAME,
            'user': DB_USER,
            'password': DB_PASS,
            'host': DB_HOST,
            'port': DB_PORT
        }
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute('SET session "my.app_user" = %s;', (user,))
        cursor.execute(query, params)  # Usamos parámetros

        inserted_id = 0

        if "INSERT" in query.upper() and "RETURNING" in query.upper():
            inserted_id = cursor.fetchone()[0]

        if "UPDATE" in query.upper() and "RETURNING" in query.upper():
            inserted_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        if inserted_id > 0:
            return inserted_id
        else:
            return True

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    

    