import json
import postgre

def lambda_handler(event, context):

    username = event['queryStringParameters']['username']

    body = json.loads(event['body'])
    
    if 'cat_id' in event['body']:
        cat_id = body['cat_id']
        language = body['language']
        value = body['value']
        state = body.get('state', '')

    query = "update categories_translations set value = '"+ value +"', state = '"+ state +"' where cat_id = '"+ cat_id +"' and language = '"+ language +"'"

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
