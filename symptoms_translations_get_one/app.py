import json
import postgre

def lambda_handler(event, context):
    sym_id = event['queryStringParameters']['sym_id']

    query = "select * from symptoms_translations where sym_id = '"+ sym_id +"' "
    results = postgre.query_postgresql(query)
    
    output = [{"sym_id": row[0],"language": row[1],"value": row[2],"state": row[3],"username": row[4]} for row in results]
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
