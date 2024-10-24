import json
import postgre

def lambda_handler(event, context):
    pat_id = event['queryStringParameters']['pat_id']
    sym_id = event['queryStringParameters']['sym_id']
    state = event['queryStringParameters']['state']
    username = event['queryStringParameters']['username']
    link = event['queryStringParameters']['link']

    query = "insert into pathologies_symptoms (pat_id, sym_id, state, username, link) values ('"+ pat_id +"', '"+ sym_id +"', '"+ state +"', '"+ username +"', '"+ link +"')"
 
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
