import json
import postgre

def lambda_handler(event, context):
    try:
        print("event", event)
    
        body = json.loads(event['body'])
        
        if 'body' in event:
            action = body['action']
            data = body['data']
        else:
            action = event['action']
            data = event['data']
            
        if action == "createPat":
            result = createPat(body)
        
        ##Add diferents actions
        if action == "get_all":
            result = createPat(data) ##replace for the correct method
        
        if action == "get_one":
            result = createPat(data) ##replace for the correct method
            
        if action == "add":
            result = createPat(data) ##replace for the correct method
            
        if action == "edit":
            result = createPat(data) ##replace for the correct method
            
        if action == "validate":
            result = createPat(data) ##replace for the correct method
            
        if action == "get_symptoms":
            result = createPat(data) ##replace for the correct method
            
        if action == "get_relations":
            result = createPat(data) ##replace for the correct method
        
        if action == "validate_relations":
            result = createPat(data) ##replace for the correct method
         
        
        if result:
            return {
                "statusCode": 200,
                "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                        },
                "body": json.dumps({
                    "message": "Success",
                    "pat_id": result,
                    "result": result
                })
            }
        else:
            raise Exception("Some error")
    
    
        
    except Exception as e:
        print("Error", e)
        return {
            "statusCode": 500,
            "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                    },
            "body": json.dumps({
                "message": "Error",
                "result": e
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
        
        #Datos pat_id de la madre
        mother = data['mother']
        
        #Datos de los lenguajes
        languages = data["languages"]
        
        #Datos de los codigos
        codes = data["codes"]
        
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
                        '{username}',
                        '{type}'
                        )
                        RETURNING pat_id; """
                        
        pat_id = postgre.insert_postgresql(query)
        print(pat_id)
        
        if pat_id:
            
            # Creo la relación con la madre solo si mother no está vacío
            if mother:
                query = f"""
                    INSERT INTO pathologies_pathologies (pat_id_1, pat_id_2, state, username)
                    VALUES (
                        '{escape_apostrophes(mother)}',
                        '{escape_apostrophes(pat_id)}',
                        'pending',
                        '{escape_apostrophes(username)}'
                    )
                """
                postgre.insert_withoutId(query)
            
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
        
            # Creo los codigos
            for code in codes:
                query = f""" INSERT INTO pathologies_codes (pat_id, code_id, value, name, state, date, username)
                                VALUES (
                                '{pat_id}',
                                '{code["code_id"]}',
                                '{escape_apostrophes(code["value"])}',
                                '{escape_apostrophes(code["name"])}',
                                'pending',
                                NOW(),
                                '{username}'
                                ); """
                postgre.insert_withoutId(query)
        
        return pat_id
    except Exception as e:
        print("error", e)
        return False
    
def escape_apostrophes(text):
    """funcion que modifica las comillas simples duplicándolas para SQL seguro."""
    if text is None:
        return ''
    return text.replace("'", "''")