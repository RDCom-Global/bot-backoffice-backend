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
    
    if 'sym_id' in event['body']:
        sym_id = body['sym_id']
        language = body['language']
        value = escape_apostrophes(body['value'])
        state = body.get('state', '')

    query = "insert into symptoms_translations (sym_id, language, value, state, username) values ('"+ sym_id +"', '"+ language +"', '"+ value +"', '"+ state +"', '"+ username +"') "

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
