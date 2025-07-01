import json
import postgre

def lambda_handler(event, context):
    
    query = "select * from pathologies order by name ASC"
    results = postgre.query_postgresql(query)
    
    output = [{"pat_id": row[0],"name": row[1],"orpha_id": row[2],"omim_id": row[3],"type": row[6]} for row in results]
    
    return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps(output)
        }
