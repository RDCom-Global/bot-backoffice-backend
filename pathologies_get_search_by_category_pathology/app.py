import json
import postgre

def lambda_handler(event, context):
    palabra = event['queryStringParameters']['palabra']

    query = "select pathologies.pat_id, pathologies_categories.cat_id, pathologies.name , pathologies.orpha_id, pathologies.omim_id from (pathologies inner join pathologies_categories on pathologies_categories.pat_id = pathologies.pat_id) where pathologies_categories.cat_id = '"+ palabra +"'"
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
