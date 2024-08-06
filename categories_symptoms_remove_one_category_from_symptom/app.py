import json
import postgre

def lambda_handler(event, context):
    cat_id = event['queryStringParameters']['cat_id']
    sym_id = event['queryStringParameters']['sym_id']

    query = "delete from categories_symptoms where (cat_id = '"+ cat_id +"' AND sym_id = '"+ sym_id +"')"
    
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
