import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']
    cat_id = event['body']['cat_id']
    name = event['body']['name']
    type = event['body']['type']

    query = "update categories set cat_id = '"+ cat_id +"', name = '"+ name +"', type = '"+ type +"' where cat_id = '"+ id +"' RETURNING *"

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
