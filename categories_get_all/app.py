import json
import postgre

def lambda_handler(event, context):
    
    
    query = "select * from categories where categories.type = 'system'"
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
