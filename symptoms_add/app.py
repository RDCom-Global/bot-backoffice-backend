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
    
    results = createSym(body)
    
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
            "sym_id": results,
            "result": results
        })
    }

def createSym(data):
    try:
        print("Data en create", data)
        
        #Datos del sintoma
        name = data["name"]
        hpo_id = data["hpo_id"]
        synonymous = data["synonymous"]
        username = data["username"]
        
        #Datos de los lenguajes
        languages = data["languages"]
        
        #Datos de la patologia
        pat_id = data["pat_id"]
        important = data["important"]
        frecuency = data["frecuency"]
        link = data["link"]
        
        # Creo el síntoma
        query = f""" INSERT INTO Symptoms (name, sym_id, hpo_id, synonymous, state, username)
                        VALUES (
                        '{escape_apostrophes(name)}',
                        (
                            SELECT 'SYM_' || LPAD(CAST(COALESCE(MAX(CAST(SUBSTRING(sym_id FROM 5) AS INTEGER)), 0) + 1 AS TEXT), 6, '0')
                            FROM Symptoms
                        ),
                        '{hpo_id}',
                        '{synonymous}',
                        'pending',
                        '{username}'
                        )
                        RETURNING sym_id; """
                        
        sym_id = postgre.insert_postgresql(query)
        print(sym_id)
        
        if sym_id:
            if pat_id != "":
                # Asocio a patologia, si es que viene patologia
                query = f""" insert into pathologies_symptoms (pat_id, sym_id, state, username, link, important, frequency) 
                        values ('{pat_id}', '{sym_id}', 'pending', '{username}', '{link}', '{important}', '{frecuency}') """
                results = postgre.insert_withoutId(query)
                
                if results is None:
                    #Aca deberiamos eliminar el síntoma
                    return False
            
            # Creo los traducciones
            for lang in languages:
                query = f""" INSERT INTO symptoms_translations (sym_id, language, value, state, username)
                                VALUES (
                                '{sym_id}',
                                '{lang["language"]}',
                                '{escape_apostrophes(lang["value"])}',
                                'pending',
                                '{username}'
                                ); """
                postgre.insert_withoutId(query)
        
        
        return sym_id
    except Exception as e:
        print("error", e)
        return False