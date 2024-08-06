import json
import postgre

def lambda_handler(event, context):
    
    query = "select * from symptoms where state='pendiente de verificar'"
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
