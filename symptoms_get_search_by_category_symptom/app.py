import json
import postgre

def lambda_handler(event, context):
    palabra = event['queryStringParameters']['palabra']

    query = "select categories_symptoms.cat_id, categories_symptoms.sym_id, symptoms.name, symptoms.hpo_id from (categories_symptoms inner join symptoms on categories_symptoms.sym_id = symptoms.sym_id) where categories_symptoms.cat_id = '"+ palabra +"'"
    results = postgre.query_postgresql(query)
    
    output = [{"cat_id": row[0],"sym_id": row[1],"name": row[2],"hpo_id": row[3]} for row in results]
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
