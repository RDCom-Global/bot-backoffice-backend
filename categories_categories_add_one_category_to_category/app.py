import json
import postgre

def lambda_handler(event, context):
    state = event['queryStringParameters']['state']
    username = event['queryStringParameters']['username']
    cat_id_1 = event['queryStringParameters']['cat_id_1']
    cat_id_2 = event['queryStringParameters']['cat_id_2']

    query = "insert into categories_categories (cat_id_1, cat_id_2, state, username) values ('"+ cat_id_1 +"', '"+ cat_id_2 +"', '"+ state +"', '"+ username +"')"
    
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
