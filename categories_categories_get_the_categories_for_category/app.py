import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']

    query = "select categories_categories.cat_id_1, categories_categories.cat_id_2, categories.name, categories.type from (categories_categories inner join categories on categories_categories.cat_id_2 = categories.cat_id) where categories_categories.cat_id_1 = '"+ id +"'"
    
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
