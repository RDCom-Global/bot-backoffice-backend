import json
import postgre

def lambda_handler(event, context):
    cat_id = event['body']['cat_id']
    name = event['body']['name']
    type = event['body']['type']

    query = "insert into categories (cat_id, name, type) values ('"+ cat_id +"', '"+ name +"', '"+ type +"') RETURNING *"

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
