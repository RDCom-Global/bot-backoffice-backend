import json
import postgre

def lambda_handler(event, context):
    pat_id = event['queryStringParameters']['pat_id']
    sym_id = event['queryStringParameters']['sym_id']

    query = "insert into pathologies_symptoms (pat_id, sym_id) values ('"+ pat_id +"', '"+ sym_id +"') RETURNING *"
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
