import json
import postgre

def lambda_handler(event, context):
    
    query = "select MAX(symptoms.hpo_id) from symptoms WHERE hpo_id LIKE 'RDC%'"
    results = postgre.query_postgresql(query)

    output = [{"max": row[0]} for row in results]
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
