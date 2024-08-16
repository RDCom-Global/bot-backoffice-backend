import json
import postgre

def lambda_handler(event, context):

    id = event['queryStringParameters']['id']

    pat_id = event['body']['pat_id']
    name = event['body']['name']
    orpha_id = event['body']['orpha_id']
    omim_id = event['body']['omim_id']

    query = "update pathologies set pat_id = '"+ pat_id +"', name = '"+ name +"', orpha_id = '"+ orpha_id +"',  omim_id = '"+ omim_id +"' where pat_id = '"+ id +"' RETURNING *"

    results = postgre.query_postgresql(query)
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(results)
    }
