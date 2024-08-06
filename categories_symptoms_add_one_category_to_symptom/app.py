import json
import postgre

def lambda_handler(event, context):
    cat_id = event['queryStringParameters']['cat_id']
    sym_id = event['queryStringParameters']['sym_id']

    query = "insert into categories_symptoms (cat_id, sym_id) values ('"+ cat_id +"', '"+ sym_id +"') RETURNING *"
    
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
