import json
import postgre

def lambda_handler(event, context):
    palabra = event['queryStringParameters']['palabra']

    query = "select * from symptoms where name ilike '%'|| '"+ palabra +"' ||'%'"

    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
