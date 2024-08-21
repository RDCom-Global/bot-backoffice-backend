import json
import postgre

def lambda_handler(event, context):
    pat_id = event['body']['pat_id']
    name = event['body']['name']
    orpha_id = event['body']['orpha_id']
    omim_id = event['body']['omim_id']

    query = "insert into pathologies (pat_id, name, orpha_id, omim_id) values ('"+ pat_id +"', '"+ name +"', '"+ orpha_id +"', '"+ omim_id +"') "

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
