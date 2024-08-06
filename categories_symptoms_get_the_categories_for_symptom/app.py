import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']

    query = "select * from categories where cat_id = '"+ id +"'"
    
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
