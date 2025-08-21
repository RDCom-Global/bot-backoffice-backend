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
            
        if action == "createSym":   ##crea una nuevo sintoma con todos los datos completos
            result = createSym(data) 
        
        if action == "get_all":   ##trae todos los sintomas
            result = getAll(data) 
            
        if action == "get_word":   ##trae todos los sintomas
            result = getWord(data) 
        
        if action == "get_one":   ##trae sintomas de una partologia en particular 
            result = getOne(data) 
            
        if action == "delete":    ##borra un sintoma y datos relacionados 
            result = deleteSym(data)
            
        if action == "edit":         ##edita / actualiza datos de un sintoma 
            result = updateSym(data) 
            
        if action == "validate_first":   ## valida una sintoma
            result = validateSymFirst(data) 
            
        if action == "validate_second":   ## valida una sintoma
            result = validateSymSecond(data) 
            
        if action == "get_symptoms":     ## trate todos los sintomas de una patologia
            result = getSymptoms(data) 
            
        if action == "get_relations": ##trae todas las relaciones patologia-sintoma 
            result = getRelations(data) 
        
        if action == "validate_relation": ##valida relacion patologia-sintoma 
            result = validateRelation(data) 
            
        
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
                  ##  "pat_id": result,
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

def getAll(data):
    try:
        query = "SELECT * FROM symptoms WHERE status NOT IN ('pending', 'inactive') ORDER BY name ASC"

        results = postgre.query_postgresql(query)

        output = [{
            "sym_id": row[0],
            "name": row[1],
            "synonymous": row[2],
            "state": row[3],
            "link": row[4],
            "hpo_id": row[5],
            "external_id": row[6]
        } for row in results]

        return output
    except Exception as e:
        print("error getAll", e)
        return False

def getWord(data):
    try:
    
        palabra = data.get("palabra", "")
    
        query = """
            SELECT * 
            FROM symptoms 
            WHERE name ILIKE %s 
               OR synonymous ILIKE %s
        """

        like_pattern = f"%{palabra}%"  
        
        results = postgre.db_read(query, params=(like_pattern, like_pattern), user="system")
        
        output = [{
            "sym_id": row[0],
            "name": row[1],
            "synonymous": row[2],
            "state": row[3],
            "link": row[4],
            "hpo_id": row[5],
            "external_id": row[6]
        } for row in results]

        return output
    except Exception as e:
        print("error getAll", e)
        return False
    
def getOne(data):
    try:
        sym_id = data.get("id", "")

        # Sintoma principal
        query_sym = "SELECT * FROM symptoms WHERE id_symptom = %s"
        results_sym = postgre.db_read(query_sym, params=(sym_id,), user="system")
        symptom = [{
            "sym_id": row[0],
            "name": row[1],
            "synonymous": row[2],
            "state": row[3],
            "link": row[4],
            "hpo_id": row[5],
            "external_id": row[6]
        } for row in results_sym]

        # Idiomas
        query_langs = "SELECT * FROM tl_symtoms WHERE id_symptom = %s"
        results_langs = postgre.db_read(query_langs, params=(sym_id,), user="system")
        idiomas = [{
            "sym_id": row[0],
            "language": row[1],
            "value": row[2],
            "state": row[3]
        } for row in results_langs]

        # Devolvemos todo en un solo JSON
        return {
            "symptom": symptom,
            "idiomas": idiomas
        }

    except Exception as e:
        print("error getOne", e)
        return False    

def createSym(data):
    try:
        #Datos del sintoma
        name = data.get("name", "")
        hpo_id = data.get("hpo_id", "")
        synonymous = data.get("synonymous", "")
        username = data.get("username", "")
       
        #Datos de los lenguajes
        languages = data.get("languages", "")
        
        #Datos de la patologia
        pat_id = data.get("pat_id", "")
        important = data.get("important", "")
        frecuency = data.get("frecuency", "")
        link = data.get("link", "")
        
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
            query = "insert into pathologies_symptoms (pat_id, sym_id, state, username, link, importante, frequency) values ('"+ pat_id +"', '"+ sym_id +"', 'pending', '"+ username +"', '"+ link +"', '"+ str(important) +"', '"+ frecuency +"')"
            results = postgre.insert_withoutId(query)
            
            if results is None:
                #Aca deberiamos eliminar el síntoma
                return False
            
            # Creo los traducciones
            for lang in languages:
                query = f""" INSERT INTO tl_symtoms (sym_id, language, value, state, username)
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
    
def updateSym(data):
    try:
        # Extraer datos
        #Datos del sintoma
        name = data.get("name", "")
        sym_id = data.get("sym_id", "")
        hpo_id = data.get("hpo_id", "")
        synonymous = data.get("synonymous", "")
        username = data.get("username", "")
        state = data.get('state', '')
        
        #Datos de los lenguajes
        languages = data.get("languages", "")
        
        #Datos de la patologia
        pat_id = data.get("pat_id", "")
        important = data.get("important", "")
        frecuency = data.get("frecuency", "")
        link = data.get("link", "")
        
        # 1. Update principal
        query_update = "update symptoms set name = '"+ name +"', hpo_id = '"+ hpo_id +"', synonymous = '"+ synonymous +"', status = '"+ state +"' where id_symptom = '"+ sym_id +"'"

        postgre.db_insert(query_update, params=(name, pat_id), user=username)

        # 2. Actualizar idiomas (borrar e insertar)
        query_delete_lang = "DELETE FROM tl_symptoms WHERE id_symptom = %s"
        postgre.db_insert(query_delete_lang, params=(sym_id,), user=username)
        for lang in languages:
            query_lang = """
                INSERT INTO tl_symptoms (id_symptom, language, value, status)
                VALUES (%s, %s, %s, 'pending')
            """
            postgre.db_insert(query_lang, params=(sym_id, lang["language"], lang["value"]), user=username)

        return sym_id

    except Exception as e:
        print("error updatePat", e)
        return False
    
def validateSymFirst(data):
    try:
 
        sym_id = data.get("sym_id", "")
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        query = "UPDATE symptoms SET status = 'verified' WHERE id_symptom = %s"
        result = postgre.db_insert(query, params=(sym_id,),user=username)
        return result
    except Exception as e:
        print("error validatePat", e)
        return False
    
def validateSymSecond(data):
    try:
 
        sym_id = data.get("sym_id", "")
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        query = "UPDATE symptoms SET status = 'active' WHERE id_symptom = %s"
        result = postgre.db_insert(query, params=(sym_id,),user=username)
        return result
    except Exception as e:
        print("error validatePat", e)
        return False
    
def getSymptoms(data):
    try:
        pat_id = data.get("id","")

        query = """
           SELECT 
            pathologies_symptoms.id_pathology, 
            symptoms.name, 
            symptoms.synonymous, 
            symptoms.id_symptom, 
            symptoms.hpo_id, 
            symptoms.status, 
            pathologies_symptoms.link, 
            pathologies_symptoms.status, 
            pathologies_symptoms.importante, 
            pathologies_symptoms.frequency  
        FROM 
            pathologies_symptoms 
        INNER JOIN 
            symptoms 
        ON 
            pathologies_symptoms.id_symptom = symptoms.id_symptom 
        WHERE 
            pathologies_symptoms.id_pathology = %s
            AND symptoms.status != 'inactive'
        ORDER BY 
            pathologies_symptoms.status DESC, 
            symptoms.name ASC
        """

        results = postgre.db_read(query, params=(pat_id,), user="system")

        output = [{
            "pat_id": row[0],
            "name": row[1],
            "synonymous": row[2],
            "sym_id": row[3],
            "hpo_id": row[4],
            "state": row[5],
            "link": row[6],
            "relstate": row[7],
            "important": row[8],
            "frequency": row[9]
        } for row in results]

        return output

    except Exception as e:
        print("error getSymptoms", e)
        return False

def deleteSym(data):
    try:
        sym_id = data.get("id","")
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        # 1. Borro idiomas
        query_delete_lang = "DELETE FROM tl_symptoms WHERE id_symptom = %s"
        postgre.db_insert(query_delete_lang, params=(sym_id,), user=username)
            
        # 3. Borro relaciones patologia-sintoma (ESTO VER CON SALI!!!!!!!!!!)
        query_delete_relations = "DELETE FROM pathologies_symptoms WHERE id_symptom = %s"
        postgre.db_insert(query_delete_relations, params=(sym_id,), user=username)
        
        # 3. Borro el sintoma principal
        query_delete_sym = "DELETE FROM symptoms WHERE id_symptom = %s"
        postgre.db_insert(query_delete_sym, params=(sym_id,), user=username)
        
        return True

    except Exception as e:
        print("error deletePat", e)
        return False

def getRelations(data):
    try:
        query = """
            SELECT 
                pp.id_pathology_1, 
                p1.name AS name_1, 
                pp.id_pathology_2, 
                p2.name AS name_2, 
                pp.state, 
                pp.username 
            FROM pathologies_pathologies pp 
            INNER JOIN pathologies p1 ON pp.id_pathology_1 = p1.id_pathology 
            INNER JOIN pathologies p2 ON pp.id_pathology_2 = p2.id_pathology 
            ORDER BY name_1 ASC, name_2 ASC
        """
        
        results = postgre.query_postgresql(query)

        output = [{
            "pat_id_1": row[0],
            "name_1": row[1],
            "pat_id_2": row[2],
            "name_2": row[3],
            "state": row[4],
            "username": row[5]
        } for row in results]

        return output
    except Exception as e:
        print("error getRelations", e)
        return False

def validateRelation(data):
    try:
        pat_id_1 = data['queryStringParameters']['pat_id_1']
        pat_id_2 = data['queryStringParameters']['pat_id_2']
        username = data.get('username', 'system')

        query = """
            UPDATE pathologies_pathologies
            SET status = 'verified'
            WHERE id_pathology_1 = %s AND id_pathology_2 = %s
        """
        result = postgre.db_insert(query, user=username, params=(pat_id_1, pat_id_2))
        return result
    except Exception as e:
        print("error validateRelations", e)
        return False
    