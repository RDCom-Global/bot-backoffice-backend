import json
import postgre

def lambda_handler(event, context):

    query = "SELECT pathologies.pat_id, pathologies.name AS nombre_patologia, symptoms.sym_id, symptoms.name AS nombre_sintoma, pathologies_symptoms.username FROM pathologies_symptoms JOIN pathologies ON pathologies_symptoms.pat_id = pathologies.pat_id JOIN symptoms ON pathologies_symptoms.sym_id = symptoms.sym_id WHERE pathologies_symptoms.state = 'pending'"

    results = postgre.query_postgresql(query)
    
    output = [{"pat_id": row[0],"pat_name": row[1],"sym_id": row[2],"sym_name": row[3],"username": row[4]} for row in results]
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
