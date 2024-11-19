import json
import postgre
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    try:
        logger.info(event)
        
        query = "SELECT * FROM users"
        results = postgre.query_postgresql(query)

        # Verificar si no se encontraron resultados
        if not results:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                "body": json.dumps({"message": "Usuario no encontrado o contraseña incorrecta."})
            }
    
        # Procesa los resultados de la consulta
        output = [{"username": row[0], "password": row[1], "type": row[2], "nombre": row[3], "apellido": row[4]} for row in results]
               
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps(output)
        }
        
    except Exception as e:
        # Registrar el error en el logger
        logger.error("Ocurrió un error: %s", str(e), exc_info=True)
        
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Ocurrió un error en el servidor."})
        }