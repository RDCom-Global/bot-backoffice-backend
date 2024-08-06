import json
import postgre

def lambda_handler(event, context):
    palabra = event['queryStringParameters']['palabra']

    query = "select categories_symptoms.cat_id, categories_symptoms.sym_id, symptoms.name, symptoms.hpo_id from (categories_symptoms inner join symptoms on categories_symptoms.sym_id = symptoms.sym_id) where categories_symptoms.cat_id = '"+ palabra +"'"
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
