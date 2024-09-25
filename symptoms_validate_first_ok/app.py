import json
import postgre

def lambda_handler(event, context):

    id = event['queryStringParameters']['sym_id']

    query = "update symptoms set state = 'primera verificación ok' where sym_id = '"+ id +"'"

    results = postgre.insert_postgresql(query)
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(results)
    }
