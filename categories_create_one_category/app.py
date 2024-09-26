import json
import postgre
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):

    state = event['queryStringParameters']['state']
    username = event['queryStringParameters']['username']

    body = json.loads(event['body'])
    
    if 'cat_id' in event['body']:
        cat_id = body['cat_id']
        name = body['name']
        type = body['type']
    
    query = "insert into categories (cat_id, name, type, state, username) values ('"+ cat_id +"', '"+ name +"', '"+ type +"', '"+ state +"', '"+ username +"')"

    results = postgre.insert_postgresql(query)
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
                   },
        "body": json.dumps(results)
    }
