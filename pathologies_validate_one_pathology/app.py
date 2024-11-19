import json
import postgre

def lambda_handler(event, context):

    pat_id = event['queryStringParameters']['id']

    query = "update pathologies set state = 'verified' where pat_id = '"+ pat_id +"'"

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
