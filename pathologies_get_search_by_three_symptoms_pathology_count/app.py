import json
import postgre

def lambda_handler(event, context):
    sym_id_1 = event['queryStringParameters']['sym_id_1']
    sym_id_2 = event['queryStringParameters']['sym_id_2']
    sym_id_3 = event['queryStringParameters']['sym_id_3']

    query = "select COUNT(*) from pathologies where pat_id in ( select pat_id from pathologies_symptoms where sym_id = '"+ sym_id_1 +"' and pat_id in (select pat_id from pathologies_symptoms where sym_id = '"+ sym_id_2 +"' and pat_id in (select pat_id from pathologies_symptoms where sym_id = '"+ sym_id_3 +"')))"
   
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
