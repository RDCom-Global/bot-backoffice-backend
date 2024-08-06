import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']

    query = "select categories_symptoms.cat_id, categories_symptoms.sym_id, categories.name, categories.type from (categories_symptoms inner join categories on categories_symptoms.cat_id = categories.cat_id) where categories_symptoms.sym_id '"+ id +"'"
    
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
