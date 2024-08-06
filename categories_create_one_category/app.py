import json
import postgre

def lambda_handler(event, context):
    cat_id = event['body']['cat_id']
    name = event['body']['name']
    type = event['body']['type']

    query = "insert into categories (cat_id, name, type) values ('"+ cat_id +"', '"+ name +"', '"+ type +"') RETURNING *"

    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
