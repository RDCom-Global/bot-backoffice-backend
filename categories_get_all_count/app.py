import json
import postgre

def lambda_handler(event, context):
    query = "select COUNT(0) from categories"
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
