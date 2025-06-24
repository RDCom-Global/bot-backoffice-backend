import json
import postgre

def escape_apostrophes(text):
    """funcion que modifica las comillas simples duplicándolas para SQL seguro."""
    if text is None:
        return ''
    return text.replace("'", "''")

def lambda_handler(event, context):

    state = event['queryStringParameters']['state']
    username = event['queryStringParameters']['username']

    body = json.loads(event['body'])
    
    if 'pat_id' in event['body']:
        pat_id = body['pat_id']
        name = escape_apostrophes(body['name'])
        orpha_id = body['orpha_id']
        omim_id = body['omim_id']

    query = "insert into pathologies (pat_id, name, orpha_id, omim_id, state, username) values ('"+ pat_id +"', '"+ name +"', '"+ orpha_id +"', '"+ omim_id +"', '"+ state +"', '"+ username +"') "

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
