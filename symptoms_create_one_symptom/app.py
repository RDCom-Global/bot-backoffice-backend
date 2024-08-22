import json
import postgre

def lambda_handler(event, context):

    body = json.loads(event['body'])
    
    if 'sym_id' in event['body']:
        name = body['name']
        sym_id = body['sym_id']
        hpo_id = body['hpo_id']
        synonymous = body['synonymous']
        link = body['link']
        state = body['state']

    query = "insert into Symptoms (name, sym_id, hpo_id, synonymous, link, state) values ('"+ name +"', '"+ sym_id +"', '"+ hpo_id +"', '"+ synonymous +"', '"+ link +"', '"+ state +"') "

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
