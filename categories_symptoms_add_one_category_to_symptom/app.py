import json
import postgre

def lambda_handler(event, context):
    cat_id = event['queryStringParameters']['cat_id']
    sym_id = event['queryStringParameters']['sym_id']
    state = event['queryStringParameters']['state']
    username = event['queryStringParameters']['username']

    query = "insert into categories_symptoms (cat_id, sym_id, state, username) values ('"+ cat_id +"', '"+ sym_id +"', '"+ state +"', '"+ username +"') "
    
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
