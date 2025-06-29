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
        name = escape_apostrophes(body['name'])
        # sym_id = body['sym_id']
        hpo_id = body.get('hpo_id', '')
        synonymous = escape_apostrophes(body.get('synonymous', ''))
        state = body.get('state', '')
        
        # Obtengo el último sym_id desde la base
        query_max = "SELECT MAX(sym_id) FROM symptoms"
        results_max = postgre.query_postgresql(query_max)
        last_sym_id = results_max[0][0] if results_max and results_max[0][0] else "SYM_000000"

        # Genero el nuevo sym_id para hacer el insert con ese...
        dato = last_sym_id.split("_")
        numero_ultimo = int(dato[1]) + 1
        sym_id = "SYM_" + str(numero_ultimo).zfill(6)
        

    query = "insert into Symptoms (name, sym_id, hpo_id, synonymous, state, username) values ('"+ name +"', '"+ sym_id +"', '"+ hpo_id +"', '"+ synonymous +"', '"+ state +"', '"+ username +"') "

    results = postgre.insert_postgresql(query)
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps({
            "message": "Síntoma creado correctamente",
            "sym_id": sym_id,
            "result": results
        })
    }

def createSym(data):
    try:
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
        
        if sym_id:
            # Asocio a patologia
            query = "insert into pathologies_symptoms (pat_id, sym_id, state, username, link, important, frequency) values ('"+ pat_id +"', '"+ sym_id +"', 'pending', '"+ username +"', '"+ link +"', '"+ str(important) +"', '"+ frecuency +"')"
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
        
        
        return True
    except Exception as e:
        return False