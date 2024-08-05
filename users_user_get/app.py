import json
import postgre

def lambda_handler(event, context):
    try:
        username = event['queryStringParameters']['username']
        password = event['queryStringParameters']['password']

        query = "select * from users where username = '"+ username +"' and password = '" + password + "'"
        results = postgre.query_postgresql(query)
        
        return {
            'statusCode': 200,
            'body': json.dumps(results)
        }
    except:
        return {
            'statusCode': 500
        } 
