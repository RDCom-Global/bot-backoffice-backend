import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']

    query = "select pathologies_symptoms.pat_id, symptoms.name, symptoms.synonymous, symptoms.sym_id, symptoms.hpo_id from (pathologies_symptoms inner join symptoms on pathologies_symptoms.sym_id = symptoms.sym_id) where pathologies_symptoms.pat_id = '"+ id +"'"
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
