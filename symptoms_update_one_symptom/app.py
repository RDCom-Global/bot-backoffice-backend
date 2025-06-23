import json
import postgre

def escape_apostrophes(text):
    """funcion que modifica las comillas simples duplicándolas para SQL seguro."""
    if text is None:
        return ''
    return text.replace("'", "''")

def lambda_handler(event, context):

    id = event['queryStringParameters']['id']

    body = json.loads(event['body'])
    
    if 'sym_id' in event['body']:
        name = escape_apostrophes(body['name'])
        sym_id = body['sym_id']
        hpo_id = body.get('hpo_id', '')
        synonymous = escape_apostrophes(body.get('synonymous', ''))
        state = body.get('state', '')

    query = "update symptoms set name = '"+ name +"', sym_id = '"+ sym_id +"', hpo_id = '"+ hpo_id +"', synonymous = '"+ synonymous +"', state = '"+ state +"' where sym_id = '"+ id +"'"

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
