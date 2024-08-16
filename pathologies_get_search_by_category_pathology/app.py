import json
import postgre

def lambda_handler(event, context):
    palabra = event['queryStringParameters']['palabra']

    query = "select pathologies.pat_id, pathologies_categories.cat_id, pathologies.name , pathologies.orpha_id, pathologies.omim_id from (pathologies inner join pathologies_categories on pathologies_categories.pat_id = pathologies.pat_id) where pathologies_categories.cat_id = '"+ palabra +"'"
    results = postgre.query_postgresql(query)
    
    output = [{"pat_id": row[0],"cat_id": row[1],"name": row[2],"orpha_id": row[3],"omim_id": row[4]} for row in results]
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
