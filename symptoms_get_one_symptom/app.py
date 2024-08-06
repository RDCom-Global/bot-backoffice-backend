import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']

    query = "select * from symptoms where sym_id = '"+ id +"'"
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
