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
    
    if 'pat_id' in event['body']:
        pat_id = body['pat_id']
        name = escape_apostrophes(body['name'])
        orpha_id = body['orpha_id']
        omim_id = body['omim_id']

    query = "update pathologies set pat_id = '"+ pat_id +"', name = '"+ name +"', orpha_id = '"+ orpha_id +"',  omim_id = '"+ omim_id +"' where pat_id = '"+ id +"'"

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
