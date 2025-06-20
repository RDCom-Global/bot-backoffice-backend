import json
import postgre

def lambda_handler(event, context):

    query = "SELECT COUNT(*) FROM pathologies_symptoms JOIN pathologies ON pathologies_symptoms.pat_id = pathologies.pat_id JOIN symptoms ON pathologies_symptoms.sym_id = symptoms.sym_id WHERE pathologies_symptoms.state = 'pending'"

    results = postgre.query_postgresql(query)
    
    output = [{"count": row[0]} for row in results]
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
