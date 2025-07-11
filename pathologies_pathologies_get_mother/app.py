import json
import postgre

def lambda_handler(event, context):
    pat_id = event['queryStringParameters']['pat_id']

    query = "select * from pathologies_pathologies where pat_id_2 = '"+ pat_id +"' "
    
    results = postgre.query_postgresql(query)
    
    output = [{"pat_id_1": row[0],"pat_id_2": row[1],"state": row[2], "username": row[3]} for row in results]
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
