import json
import postgre

def lambda_handler(event, context):
    
    query = "select COUNT(*) from pathologies"
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

