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
    
    if 'pat_id' in body:
        pat_id = body['pat_id']
        code_id = body['code_id']
        value = escape_apostrophes(body['value'])
        name = escape_apostrophes(body['name'])
        state = body['state']

    query = "update pathologies_codes set code_id = '"+ code_id +"', value = '"+ value +"', name = '"+ name +"', state = '"+ state +"', date = NOW(), username = '"+ username +"' where pat_id = '"+ pat_id +"' and code_id = '"+ code_id +"' and value = '"+ value +"'"

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
