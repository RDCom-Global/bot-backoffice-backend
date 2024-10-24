import json
import postgre

def lambda_handler(event, context):

    username = event['queryStringParameters']['username']

    body = json.loads(event['body'])
    
    if 'sym_id' in event['body']:
        name = body['name']
        sym_id = body['sym_id']
        hpo_id = body.get('hpo_id', '')
        synonymous = body.get('synonymous', '')
        state = body.get('state', '')

    query = "insert into Symptoms (name, sym_id, hpo_id, synonymous, state, username) values ('"+ name +"', '"+ sym_id +"', '"+ hpo_id +"', '"+ synonymous +"', '"+ state +"', '"+ username +"') "

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
