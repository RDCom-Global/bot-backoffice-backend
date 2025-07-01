import json
import postgre

def escape_apostrophes(text):
    """funcion que modifica las comillas simples duplicándolas para SQL seguro."""
    if text is None:
        return ''
    return text.replace("'", "''")

def lambda_handler(event, context):

    print("event", event)
    
    body = json.loads(event['body'])
    
    results = createPat(body)
    
    if results == False:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({
                "message": "Error al crear el síntoma",
                "result": results
            })
        }
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps({
            "message": "Síntoma creado correctamente",
            "pat_id": results,
            "result": results
        })
    }

def createPat(data):
    try:
        print("Data en create", data)
        
        #Datos de la patologia
        
        name = escape_apostrophes(data["name"])
        orpha_id = data["orpha_id"]
        omim_id = data["omim_id"]
        type = data['type']
        username = data["username"]
        
        #Datos de los lenguajes
        languages = data["languages"]
        
        
        # Creo la patologia
        query = f""" INSERT INTO pathologies (name, pat_id, orpha_id, omim_id, state, username, type)
                        VALUES (
                        '{escape_apostrophes(name)}',
                        (
                            SELECT 'PAT_' || LPAD(CAST(COALESCE(MAX(CAST(SUBSTRING(pat_id FROM 5) AS INTEGER)), 0) + 1 AS TEXT), 6, '0')
                            FROM pathologies
                        ),
                        '{orpha_id}',
                        '{omim_id}',
                        'pending',
                        '{username}'
                        '{type}'
                        )
                        RETURNING pat_id; """
                        
        pat_id = postgre.insert_postgresql(query)
        print(pat_id)
        
        if pat_id:
            
            # Creo los traducciones
            for lang in languages:
                query = f""" INSERT INTO pathologies_translations (pat_id, language, value, state, username)
                                VALUES (
                                '{pat_id}',
                                '{lang["language"]}',
                                '{escape_apostrophes(lang["value"])}',
                                'pending',
                                '{username}'
                                ); """
                postgre.insert_withoutId(query)
        
        
        return pat_id
    except Exception as e:
        print("error", e)
        return False