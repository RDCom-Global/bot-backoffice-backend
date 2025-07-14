import json
import postgre

def lambda_handler(event, context):
    pat_id_1 = event['queryStringParameters']['pat_id_1']
    pat_id_2 = event['queryStringParameters']['pat_id_2']

    query = "update pathologies_pathologies set state = 'verified' where pat_id_1 = '"+ pat_id_1 +"' and pat_id_2 = '"+ pat_id_2 +"'"
 
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
