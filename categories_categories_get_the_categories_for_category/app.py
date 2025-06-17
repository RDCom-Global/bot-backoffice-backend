import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']

    query = "select categories_categories.cat_id_1, categories_categories.cat_id_2, categories.name, categories.type from (categories_categories inner join categories on categories_categories.cat_id_2 = categories.cat_id) where categories_categories.cat_id_1 = '"+ id +"' ORDER BY categories.name ASC"
    
    results = postgre.query_postgresql(query)
    
    output = [{"cat_id_1": row[0],"cat_id_2": row[1],"name": row[2],"type": row[3]} for row in results]

    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
