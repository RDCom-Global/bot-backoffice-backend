import json
import postgre

def lambda_handler(event, context):
    pat_id = event['queryStringParameters']['pat_id']

    query = "SELECT pp.pat_id_1, p1.name AS name_1, pp.pat_id_2, p2.name AS name_2, pp.state, pp.username FROM pathologies_pathologies pp INNER JOIN pathologies p1 ON pp.pat_id_1 = p1.pat_id INNER JOIN pathologies p2 ON pp.pat_id_2 = p2.pat_id WHERE pp.pat_id_2 = '" + pat_id + "' ORDER BY name_1 ASC, name_2 ASC"
    
    results = postgre.query_postgresql(query)
    
    output = [{"pat_id_1": row[0],"name_1": row[1],"pat_id_2": row[2],"name_2": row[3],"state": row[4], "username": row[5]} for row in results]
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
