import json
import postgre

def lambda_handler(event, context):

    id = event['queryStringParameters']['id']

    body = json.loads(event['body'])
    
    if 'sym_id' in event['body']:
        name = body['name']
        sym_id = body['sym_id']
        hpo_id = body['hpo_id']
        synonymous = body['synonymous']
        link = body['link']
        state = body['state'] 

    query = "update symptoms set name = '"+ name +"', sym_id = '"+ sym_id +"', hpo_id = '"+ hpo_id +"', synonymous = '"+ synonymous +"', link = '"+ link +"', state = '"+ state +"' where sym_id = '"+ id +"'"

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
