import json
import postgre

def lambda_handler(event, context):
    pat_id = event['queryStringParameters']['pat_id']
    sym_id = event['queryStringParameters']['sym_id']

    query = "delete from pathologies_symptoms where (pat_id = '"+ pat_id +"' AND sym_id = '"+ sym_id +"')"
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
