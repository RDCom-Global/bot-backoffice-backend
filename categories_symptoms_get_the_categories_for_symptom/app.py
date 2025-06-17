import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']

    query = "select categories_symptoms.cat_id, categories_symptoms.sym_id, categories.name, categories.type from (categories_symptoms inner join categories on categories_symptoms.cat_id = categories.cat_id) where categories_symptoms.sym_id = '"+ id +"' ORDER BY categories.name ASC"
    
    results = postgre.query_postgresql(query)
    
    output = [{"cat_id": row[0],"sym_id": row[1],"name": row[2],"type": row[3]} for row in results]
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
