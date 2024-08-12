import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']

<<<<<<< HEAD
    query = "select categories_symptoms.cat_id, categories_symptoms.sym_id, categories.name, categories.type from (categories_symptoms inner join categories on categories_symptoms.cat_id = categories.cat_id) where categories_symptoms.sym_id '"+ id +"'"
=======
    query = "select * from categories where cat_id = '"+ id +"'"
>>>>>>> ba363feff47f235e8466f1cff5db82bbc74919a7
    
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
