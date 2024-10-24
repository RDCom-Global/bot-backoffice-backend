import json
import postgre

def lambda_handler(event, context):
        
    body = json.loads(event['body'])
    
    if 'pat_id' in event['body']:
        pat_id = body['pat_id']
        sym_id = body['sym_id']
        link = body.get('link', '')

    query = "update pathologies_symptoms set link = '"+ link +"' where pat_id = '"+ pat_id +"' and sym_id = '"+ sym_id +"'"
 
    results = postgre.insert_postgresql(query)
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(results)
    }
