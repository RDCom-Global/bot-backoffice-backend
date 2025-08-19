import json
import postgre

def lambda_handler(event, context):
    pat_id = event['queryStringParameters']['pat_id']

    query = "select * from pathologies_codes where id_pathology = '"+ pat_id +"' "
    results = postgre.query_postgresql(query)
    
    output = [{"pat_id": row[0],"code_id": row[1],"value": row[2],"name": row[3],"state": row[4]} for row in results]
    
    return {
    "statusCode": 200,
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    },
    "body": json.dumps({
        "message": "Success",
        "result": output
    })
}
