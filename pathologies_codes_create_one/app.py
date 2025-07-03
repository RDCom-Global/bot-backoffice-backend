import json
import postgre

def escape_apostrophes(text):
    """funcion que modifica las comillas simples duplicándolas para SQL seguro."""
    if text is None:
        return ''
    return text.replace("'", "''")

def lambda_handler(event, context):

    username = event['queryStringParameters']['username']

    body = json.loads(event['body'])
    
    if 'pat_id' in event['body']:
        pat_id = body['pat_id']
        code_id = body['code_id']
        value = escape_apostrophes(body['value'])
        name = escape_apostrophes(body['name'])
        state = body['state']

    query = "insert into pathologies_codes (pat_id, code_id, value, name, state, date, username) values ('"+ pat_id +"', '"+ code_id +"', '"+ value +"', '"+ name +"', '"+ state +"', NOW(), '"+ username +"') "

    results = postgre.insert_postgresql(query)
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(results)
    }
