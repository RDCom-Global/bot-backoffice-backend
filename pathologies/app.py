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
            
        if action == "createPat":   ##ESTA REPETIDA ESTA FUNCION...
            result = createPat(body) ##ESTA REPETIDA ESTA FUNCION...
        
        if action == "get_all":   ##trae todas las patologias 
            result = getAll(data) 
        
        if action == "get_one":   ##trae datos de una en particular 
            result = getOne(data) 
            
        if action == "add":           ##ESTA REPETIDA ESTA FUNCION....
            result = createPat(data)  ##ESTA REPETIDA ESTA FUNCION...
            
        if action == "delete":    ##borra una patologia y datos relacionados 
            result = deletePat(data)
            
        if action == "edit":         ##edita / actualiza datos de una en particular 
            result = updatePat(data) 
            
        if action == "validate":   ## valida una patologia
            result = validatePat(data) 
            
        if action == "get_symptoms":     ## trate todos los sintomas de una patologia
            result = getSymptoms(data) 
            
        if action == "get_relations": ##trae todas las relaciones madre-hija 
            result = getRelations(data) 
        
        if action == "validate_relation": ##valida relacion madre-hija
            result = validateRelation(data) 
            
        if action == "get_mother":  ##trae la madre 
            result = getMother(data)   
         
        
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
        query = """
            SELECT 
                p.pat_id,
                p.name,
                p.orpha_id,
                p.omim_id,
                p.type,
                p.state,
                COALESCE(
                    STRING_AGG(pc.code_id || ':' || pc.value, ', '), ''
                ) AS codes
            FROM pathologies p
            LEFT JOIN pathologies_codes pc ON p.pat_id = pc.pat_id AND pc.state != 'inactive'
            GROUP BY p.pat_id, p.name, p.orpha_id, p.omim_id, p.type
            ORDER BY p.name ASC;
        """

        results = postgre.query_postgresql(query)

        output = [{
            "pat_id": row[0],
            "name": row[1],
            "orpha_id": row[2],
            "omim_id": row[3],
            "type": row[4],
            "state": row[5],
            "codes": row[6]
        } for row in results]

        return output
    except Exception as e:
        print("error getAll", e)
        return False
    
def getOne(data):
    try:
        pat_id = data['queryStringParameters']['id']
        
        query = "SELECT * FROM pathologies WHERE pat_id = %s"
        results = postgre.db_read(query, user="system", params=(pat_id,))

        output = [{"pat_id": row[0], "name": row[1], "orpha_id": row[2], "omim_id": row[3], "type": row[6]} for row in results]
        return output
    except Exception as e:
        print("error getOne", e)
        return False
    

def createPat(data):
    try:
        name = data["name"]
        orpha_id = data["orpha_id"]
        omim_id = data["omim_id"]
        type = data["type"]
        username = data["username"]
        mother = data["mother"]
        languages = data["languages"]
        codes = data["codes"]

        # Obtengo nuevo pat_id dinámicamente
        query_pat_id = """
            SELECT 'PAT_' || LPAD(CAST(COALESCE(MAX(CAST(SUBSTRING(pat_id FROM 5) AS INTEGER)), 0) + 1 AS TEXT), 6, '0')
            FROM pathologies
        """
        pat_id_result = postgre.db_read(query_pat_id, user=username)
        pat_id = pat_id_result[0][0]

        # Insert principal
        query_insert = """
            INSERT INTO pathologies (name, pat_id, orpha_id, omim_id, state, username, type)
            VALUES (%s, %s, %s, %s, 'pending', %s, %s)
        """
        postgre.db_insert(query_insert, user=username, params=(name, pat_id, orpha_id, omim_id, username, type))

        # Inserto madre (si hay)
        if mother:
            query_mother = """
                INSERT INTO pathologies_pathologies (pat_id_1, pat_id_2, state, username)
                VALUES (%s, %s, 'pending', %s)
            """
            postgre.db_insert(query_mother, user=username, params=(mother, pat_id, username))

        # Inserto Traducciones
        for lang in languages:
            query_lang = """
                INSERT INTO pathologies_translations (pat_id, language, value, state, username)
                VALUES (%s, %s, %s, 'pending', %s)
            """
            postgre.db_insert(query_lang, user=username, params=(pat_id, lang["language"], lang["value"], username))

        # Inserto Códigos
        for code in codes:
            query_code = """
                INSERT INTO pathologies_codes (pat_id, code_id, value, name, state, date, username)
                VALUES (%s, %s, %s, %s, 'pending', NOW(), %s)
            """
            postgre.db_insert(query_code, user=username, params=(pat_id, code["code_id"], code["value"], code["name"], username))

        return pat_id

    except Exception as e:
        print("error createPat", e)
        return False
    
def updatePat(data):
    try:
        pat_id = data["pat_id"]
        name = data["name"]
        orpha_id = data["orpha_id"]
        omim_id = data["omim_id"]
        type = data["type"]
        username = data["username"]
        mother = data["mother"]
        languages = data["languages"]
        codes = data["codes"]

        # 1. Update principal
        query_update = """
            UPDATE pathologies
            SET name = %s, orpha_id = %s, omim_id = %s, type = %s, username = %s
            WHERE pat_id = %s
        """
        postgre.db_insert(query_update, user=username, params=(name, orpha_id, omim_id, type, username, pat_id))

        # 2. Actualizar madre (eliminar y agregar de nuevo si existe)
        query_delete_mother = "DELETE FROM pathologies_pathologies WHERE pat_id_2 = %s"
        postgre.db_insert(query_delete_mother, user=username, params=(pat_id,))
        if mother:
            query_mother = """
                INSERT INTO pathologies_pathologies (pat_id_1, pat_id_2, state, username)
                VALUES (%s, %s, 'pending', %s)
            """
            postgre.db_insert(query_mother, user=username, params=(mother, pat_id, username))

        # 3. Actualizar idiomas (borrar e insertar)
        query_delete_lang = "DELETE FROM pathologies_translations WHERE pat_id = %s"
        postgre.db_insert(query_delete_lang, user=username, params=(pat_id,))
        for lang in languages:
            query_lang = """
                INSERT INTO pathologies_translations (pat_id, language, value, state, username)
                VALUES (%s, %s, %s, 'pending', %s)
            """
            postgre.db_insert(query_lang, user=username, params=(pat_id, lang["language"], lang["value"], username))

        # 4. Actualizar códigos (borrar e insertar)
        query_delete_codes = "DELETE FROM pathologies_codes WHERE pat_id = %s"
        postgre.db_insert(query_delete_codes, user=username, params=(pat_id,))
        for code in codes:
            query_code = """
                INSERT INTO pathologies_codes (pat_id, code_id, value, name, state, date, username)
                VALUES (%s, %s, %s, %s, 'pending', NOW(), %s)
            """
            postgre.db_insert(query_code, user=username, params=(pat_id, code["code_id"], code["value"], code["name"], username))

        return pat_id

    except Exception as e:
        print("error updatePat", e)
        return False
    
def validatePat(data):
    try:
        pat_id = data['queryStringParameters']['id']
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        query = "UPDATE pathologies SET state = 'verified' WHERE pat_id = %s"
        result = postgre.db_insert(query, user=username, params=(pat_id,))
        return result
    except Exception as e:
        print("error validatePat", e)
        return False
    
def getSymptoms(data):
    try:
        pat_id = data['queryStringParameters']['id']

        query = """
            SELECT 
                pathologies_symptoms.pat_id, 
                symptoms.name, 
                symptoms.synonymous, 
                symptoms.sym_id, 
                symptoms.hpo_id, 
                symptoms.state, 
                pathologies_symptoms.username, 
                pathologies_symptoms.link, 
                pathologies_symptoms.state, 
                pathologies_symptoms.important, 
                pathologies_symptoms.frequency  
            FROM 
                pathologies_symptoms 
            INNER JOIN 
                symptoms 
            ON 
                pathologies_symptoms.sym_id = symptoms.sym_id 
            WHERE 
                pathologies_symptoms.pat_id = %s 
                AND symptoms.state != 'inactive'
            ORDER BY 
                pathologies_symptoms.state DESC, 
                symptoms.name ASC
        """

        results = postgre.db_read(query, params=(pat_id,))

        output = [{
            "pat_id": row[0],
            "name": row[1],
            "synonymous": row[2],
            "sym_id": row[3],
            "hpo_id": row[4],
            "state": row[5],
            "username": row[6],
            "link": row[7],
            "relstate": row[8],
            "important": row[9],
            "frequency": row[10]
        } for row in results]

        return output

    except Exception as e:
        print("error getSymptoms", e)
        return False

def deletePat(data):
    try:
        pat_id = data['queryStringParameters']['id']
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        # 1. Borro idiomas
        query_delete_lang = "DELETE FROM pathologies_translations WHERE pat_id = %s"
        postgre.db_insert(query_delete_lang, user=username, params=(pat_id,))
        
        # 2. Borro códigos
        query_delete_codes = "DELETE FROM pathologies_codes WHERE pat_id = %s"
        postgre.db_insert(query_delete_codes, user=username, params=(pat_id,))
        
        # 3. Borro relaciones madre-hijo (ESTO VER CON SALI!!!!!!!!!!)
        query_delete_mother = "DELETE FROM pathologies_pathologies WHERE pat_id_2 = %s OR pat_id_1 = %s"
        postgre.db_insert(query_delete_mother, user=username, params=(pat_id, pat_id))
        
        # 4. Borro la patología principal
        query_delete_pat = "DELETE FROM pathologies WHERE pat_id = %s"
        postgre.db_insert(query_delete_pat, user=username, params=(pat_id,))
        
        return True

    except Exception as e:
        print("error deletePat", e)
        return False

def getRelations(data):
    try:
        query = """
            SELECT 
                pp.pat_id_1, 
                p1.name AS name_1, 
                pp.pat_id_2, 
                p2.name AS name_2, 
                pp.state, 
                pp.username 
            FROM pathologies_pathologies pp 
            INNER JOIN pathologies p1 ON pp.pat_id_1 = p1.pat_id 
            INNER JOIN pathologies p2 ON pp.pat_id_2 = p2.pat_id 
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
            SET state = 'verified'
            WHERE pat_id_1 = %s AND pat_id_2 = %s
        """
        result = postgre.db_insert(query, user=username, params=(pat_id_1, pat_id_2))
        return result
    except Exception as e:
        print("error validateRelations", e)
        return False
    
def getMother(data):
    try:
        pat_id = data['queryStringParameters']['pat_id']
        username = data.get('username', 'system')  # opcional, por consistencia con otras funciones

        query = """
            SELECT 
                pat_id_1, 
                pat_id_2, 
                state, 
                username
            FROM 
                pathologies_pathologies
            WHERE 
                pat_id_2 = %s
        """

        results = postgre.db_read(query, user=username, params=(pat_id,))

        output = [{
            "pat_id_1": row[0],
            "pat_id_2": row[1],
            "state": row[2],
            "username": row[3]
        } for row in results]

        return output

    except Exception as e:
        print("error getMother", e)
        return False