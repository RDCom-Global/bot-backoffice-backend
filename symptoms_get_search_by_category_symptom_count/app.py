import json
import postgre

def lambda_handler(event, context):
    palabra = event['queryStringParameters']['palabra']

    query = "select COUNT(*) from (categories_symptoms inner join symptoms on categories_symptoms.sym_id = symptoms.sym_id) where categories_symptoms.cat_id = '"+ palabra +"'"
    results = postgre.query_postgresql(query)
    
    output = [{"count": row[0]} for row in results]
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
