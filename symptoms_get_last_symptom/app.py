import json
import postgre

def lambda_handler(event, context):
    
    query = "select MAX(symptoms.sym_id) from symptoms"
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
