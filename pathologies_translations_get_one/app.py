import json
import postgre

def lambda_handler(event, context):
    pat_id = event['queryStringParameters']['id']

    query = "select * from tl_pathologies where id_pathology = '"+ pat_id +"' "
    results = postgre.db_read(query)
    ##query_postgresql
    
    output = [{"pat_id": row[0],"language": row[1],"value": row[2],"state": row[3]} for row in results]
    
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
