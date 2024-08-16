import json
import postgre

def lambda_handler(event, context):
    query = "select * from symptoms where state='pendiente de verificar'"
    results = postgre.query_postgresql(query)
    
    output = [{"sym_id": row[0],"name": row[1],"state": row[2],"synonymous": row[3],"link": row[4],"hpo_id": row[5]} for row in results]
   
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
