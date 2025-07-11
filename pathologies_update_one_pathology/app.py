import json
import postgre

def escape_apostrophes(text):
    """Función que modifica las comillas simples duplicándolas para SQL seguro."""
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
        type = body['type']
        mother = body['mother']
        username = body['username']

    # Actualiza los datos principales
    query = f"""
        UPDATE pathologies
        SET
            pat_id = '{escape_apostrophes(pat_id)}',
            name = '{name}',
            orpha_id = '{orpha_id}',
            omim_id = '{omim_id}',
            type = '{type}'
        WHERE pat_id = '{id}'
    """
    results = postgre.insert_postgresql(query)

    # Si mother no está vacío, borra relación anterior e inserta nueva
    if mother:
        # Elimina cualquier relación anterior con este hijo
        delete_query = f"""
            DELETE FROM pathologies_pathologies
            WHERE pat_id_2 = '{escape_apostrophes(id)}'
        """
        postgre.insert_withoutId(delete_query)

        # Crea la nueva relación
        insert_query = f"""
            INSERT INTO pathologies_pathologies (pat_id_1, pat_id_2, state, username)
            VALUES (
                '{escape_apostrophes(mother)}',
                '{escape_apostrophes(id)}',
                'pending',
                '{escape_apostrophes(username)}'
            )
        """
        postgre.insert_withoutId(insert_query)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps(results)
    }