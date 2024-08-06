import json
import postgre

def lambda_handler(event, context):
    pat_id = event['body']['pat_id']
    name = event['body']['name']
    orpha_id = event['body']['orpha_id']
    omim_id = event['body']['omim_id']

    query = "insert into pathologies (pat_id, name, orpha_id, omim_id) values ('"+ pat_id +"', '"+ name +"', '"+ orpha_id +"', '"+ omim_id +"') RETURNING *"

    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
