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
            
        if action == "validate":   ## valida una sintoma
            result = validateSym(data) 
            
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
        pat_id = data.get("id", "")

        # Patología principal
        query_pat = "SELECT * FROM pathologies WHERE id_pathology = %s"
        results_pat = postgre.db_read(query_pat, params=(pat_id,), user="system")
        pathology = [{
            "pat_id": row[0],
            "name": row[1],
            "status": row[2],
            "external_id": row[3],
            "type": row[4]
        } for row in results_pat]

        # Madre
        query_mother = "SELECT id_pathology_1, id_pathology_2, status FROM pathologies_pathologies WHERE id_pathology_2 = %s"
        results_mother = postgre.db_read(query_mother, params=(pat_id,), user="system")
        mother = [{
            "pat_id_1": row[0],
            "pat_id_2": row[1],
            "state": row[2]
        } for row in results_mother]

        # Idiomas
        query_langs = "SELECT * FROM tl_pathologies WHERE id_pathology = %s"
        results_langs = postgre.db_read(query_langs, params=(pat_id,), user="system")
        idiomas = [{
            "pat_id": row[0],
            "language": row[1],
            "value": row[2],
            "state": row[3]
        } for row in results_langs]

        # Códigos
        query_codes = "SELECT * FROM pathologies_codes WHERE id_pathology = %s"
        results_codes = postgre.db_read(query_codes, params=(pat_id,), user="system")
        codigos = [{
            "pat_id": row[0],
            "code_id": row[1],
            "value": row[2],
            "name": row[3],
            "state": row[4]
        } for row in results_codes]

        # Devolvemos todo en un solo JSON
        return {
            "pathology": pathology,
            "mother": mother,
            "idiomas": idiomas,
            "codigos": codigos
        }

    except Exception as e:
        print("error getOne", e)
        return False    

def createSym(data):
    try:
        # Extraer datos
        name = data.get("name", "")
        type_ = data.get("type", "")
        username = data.get("username", "")
        mother = data.get("mother")  # None si no hay
        languages = data.get("languages", [])
        codes = data.get("codes", [])

        # Generar external_id
        query_ext_id = """
            SELECT 'PAT_' || LPAD(CAST(COALESCE(MAX(CAST(SUBSTRING(external_id FROM 5) AS INTEGER)), 0) + 1 AS TEXT), 6, '0')
            FROM pathologies
        """
        ext_id_result = postgre.db_read(query_ext_id)
        external_id = ext_id_result[0][0]

        # Insert principal (db_insert solo inserta)
        query_insert = """
            INSERT INTO pathologies (name, status, type, external_id)
            VALUES (%s, 'pending', %s, %s)
        """
        postgre.db_insert(query_insert, params=(name, type_, external_id), user=username)

        # Obtener id_pathology recién creado
        query_get_id = "SELECT id_pathology FROM pathologies WHERE external_id = %s"
        pat_id_result = postgre.db_read(query_get_id, params=(external_id,), user=username)
        pat_id = pat_id_result[0][0]

        # Inserto madre (si hay)
        if mother:
            query_mother = """
                INSERT INTO pathologies_pathologies (id_pathology_1, id_pathology_2, status)
                VALUES (%s, %s, 'pending')
            """
            postgre.db_insert(query_mother, params=(mother, pat_id), user=username)

        # Inserto traducciones
        for lang in languages:
            query_lang = """
                INSERT INTO tl_pathologies (id_pathology, language, value, status)
                VALUES (%s, %s, %s, 'pending')
            """
            postgre.db_insert(query_lang, params=(pat_id, lang.get("language", ""), lang.get("value", "")), user=username)

        # Inserto códigos
        for code in codes:
            query_code = """
                INSERT INTO pathologies_codes (id_pathology, id_code, value, name, status)
                VALUES (%s, %s, %s, %s, 'pending')
            """
            postgre.db_insert(query_code, params=(pat_id, code.get("code_id", ""), code.get("value", ""), code.get("name", "")), user=username)

        return pat_id

    except Exception as e:
        print("error createPat", e)
        return False
    
def updateSym(data):
    try:
        # Extraer datos
        pat_id = data.get("pat_id", "")
        name = data.get("name", "")
        type_ = data.get("type", "")
        username = data.get("username", "")
        mother = data.get("mother")  # None si no hay
        languages = data.get("languages", [])
        codes = data.get("codes", [])
        
        # 1. Update principal
        query_update = """
            UPDATE pathologies
            SET name = %s, type = %s
            WHERE id_pathology = %s
        """
        postgre.db_insert(query_update, params=(name, type_, pat_id), user=username)

        # 2. Actualizar madre (eliminar y agregar de nuevo si existe)
        query_delete_mother = "DELETE FROM pathologies_pathologies WHERE id_pathology_2 = %s"
        postgre.db_insert(query_delete_mother, params=(pat_id,), user=username)
        if mother:
            query_mother = """
                INSERT INTO pathologies_pathologies (id_pathology_1, id_pathology_2, status)
                VALUES (%s, %s, 'pending')
            """
            postgre.db_insert(query_mother, params=(mother, pat_id), user=username)

        # 3. Actualizar idiomas (borrar e insertar)
        query_delete_lang = "DELETE FROM tl_pathologies WHERE id_pathology = %s"
        postgre.db_insert(query_delete_lang, params=(pat_id,), user=username)
        for lang in languages:
            query_lang = """
                INSERT INTO tl_pathologies (id_pathology, language, value, status)
                VALUES (%s, %s, %s, 'pending')
            """
            postgre.db_insert(query_lang, params=(pat_id, lang["language"], lang["value"]), user=username)

        # 4. Actualizar códigos (borrar e insertar)
        query_delete_codes = "DELETE FROM pathologies_codes WHERE id_pathology = %s"
        postgre.db_insert(query_delete_codes, params=(pat_id,), user=username)
        for code in codes:
            query_code = """
                INSERT INTO pathologies_codes (id_pathology, id_code, value, name, status)
                VALUES (%s, %s, %s, %s, 'pending')
            """
            postgre.db_insert(query_code, params=(pat_id, code["code_id"], code["value"], code["name"]), user=username)

        return pat_id

    except Exception as e:
        print("error updatePat", e)
        return False
    
def validateSym(data):
    try:
 
        pat_id = data.get("pat_id", "")
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        query = "UPDATE pathologies SET status = 'active' WHERE id_pathology = %s"
        result = postgre.db_insert(query, params=(pat_id,),user=username)
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
        pat_id = data.get("id","")
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        # 1. Borro idiomas
        query_delete_lang = "DELETE FROM tl_pathologies WHERE id_pathology = %s"
        postgre.db_insert(query_delete_lang, params=(pat_id,), user=username)
        
        # 2. Borro códigos
        query_delete_codes = "DELETE FROM pathologies_codes WHERE id_pathology = %s"
        postgre.db_insert(query_delete_codes, params=(pat_id,), user=username)
        
        # 3. Borro relaciones madre-hijo (ESTO VER CON SALI!!!!!!!!!!)
        query_delete_mother = "DELETE FROM pathologies_pathologies WHERE id_pathology_2 = %s OR id_pathology_1 = %s"
        postgre.db_insert(query_delete_mother, params=(pat_id, pat_id), user=username)
        
        # 4. Borro la patología principal
        query_delete_pat = "DELETE FROM pathologies WHERE id_pathology = %s"
        postgre.db_insert(query_delete_pat, params=(pat_id,), user=username)
        
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
    