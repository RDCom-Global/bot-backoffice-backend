import json
import postgre

def lambda_handler(event, context):
    
    query = "select * from categories where categories.type = 'system'"
    results = postgre.query_postgresql(query)
    
    output = [{"cat_id": row[0],"name": row[1],"type": row[2]} for row in results]
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
