import json
import postgre
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    try:
        logger.info(event)
        
        username = event['queryStringParameters']['username']
        password = event['queryStringParameters']['password']

        query = "select * from users where username = '"+ username +"' and password = '" + password + "'"
        results = postgre.query_postgresql(query)
        
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps(results)
        }
        
    except Exception as e:
        # Registrar el error en el logger
        logger.error("Ocurrió un error: %s", str(e), exc_info=True)
        
        return {
            'statusCode': 500
        } 
