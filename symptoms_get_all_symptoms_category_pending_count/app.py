import json
import postgre

def lambda_handler(event, context):
    query = "SELECT COUNT(*) FROM symptoms s LEFT JOIN category_symptoms cs ON s.sym_id = cs.sym_id WHERE cs.sym_id IS NULL"
    results = postgre.query_postgresql(query)
    
    output = [{"sym_id": row[0],"name": row[1],"synonymous": row[2],"state": row[3],"link": row[4],"hpo_id": row[5],"username": row[6]} for row in results]
   
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }