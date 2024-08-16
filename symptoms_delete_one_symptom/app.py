import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']

    query = "delete from symptoms where sym_id = '"+ id +"'"

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
