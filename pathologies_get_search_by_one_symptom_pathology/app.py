import json
import postgre

def lambda_handler(event, context):
    sym_id_1 = event['queryStringParameters']['sym_id_1']

    query = "select pathologies.pat_id, pathologies.name , pathologies.orpha_id, pathologies.omim_id from (pathologies inner join pathologies_symptoms on pathologies_symptoms.pat_id = pathologies.pat_id) where pathologies_symptoms.sym_id = '"+ sym_id_1 +"'"
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
