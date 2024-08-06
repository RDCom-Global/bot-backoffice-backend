import json
import postgre

def lambda_handler(event, context):
    cat_id_1 = event['queryStringParameters']['cat_id_1']
    cat_id_2 = event['queryStringParameters']['cat_id_2']

    query = "delete from categories_categories where (cat_id_1 = '"+ cat_id_1 +"' AND cat_id_2 = '"+ cat_id_2 +"')"
    
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
