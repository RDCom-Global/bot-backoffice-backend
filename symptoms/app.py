import json
import postgre

def lambda_handler(event, context):
    try:
        print("event", event)
    
        body = json.loads(event['body'])
        
        # Extraer user_email del header X-User-Email
        user_email = event.get('headers', {}).get('x-user-email', 'system')
        
        if 'body' in event:
            action = body['action']
            data = body['data']
        else:
            action = event['action']
            data = event['data']
            
        if action == "create_sym":   ##crea una nuevo sintoma con todos los datos completos
            result = createSym(data, user_email) 
        
        if action == "get_all":   ##trae todos los sintomas
            result = getAll(data, user_email) 
            
        if action == "get_all_no_category":   ##trae todos los sintomas sin categoria asignada
            result = getAllNoCategory(data, user_email) 
            
        if action == "get_by_word":   ##trae todos los sintomas que incluyan una palabra
            result = getByWord(data, user_email) 
            
        if action == "get_by_code":   ##trae todos los sintomas que tengan el codigo de busqueda
            result = getByCode(data, user_email) 
        
        if action == "get_one":   ##trae datos de un sintoma en particular 
            result = getOne(data, user_email) 
            
        if action == "delete_sym":    ##borra un sintoma y datos relacionados 
            result = deleteSym(data, user_email)
            
        if action == "update_sym":     ##edita / actualiza datos de un sintoma 
            result = updateSym(data, user_email) 
            
        if action == "validate_first":   ## valida una sintoma
            result = validateSymFirst(data, user_email) 
            
        if action == "validate_second":   ## activa una sintoma
            result = validateSymSecond(data, user_email) 
            
        if action == "get_pending_relations": ##trae todas las relaciones patologia-sintoma pendientes
            result = getPendingRelations(data, user_email) 
        
        if action == "validate_relation": ##valida relacion patologia-sintoma 
            result = validateRelation(data, user_email) 

        if action == "delete_relation": ##borra relacion patologia-sintoma 
            result = deleteRelation(data, user_email) 
            
        if action == "create_relation": ##crea relacion patologia-sintoma 
            result = createRelation(data, user_email) 
            
        if action == "update_relation": ##actualiza relacion patologia-sintoma 
            result = updateRelation(data, user_email) 
            
        if action == "get_relation": ##busca datos de  relacion patologia-sintoma 
            result = getRelation(data, user_email)         
              
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

def getAll(data, user_email):
    try:
        query = "SELECT * FROM symptoms WHERE status NOT IN ('inactive') ORDER BY name ASC"

        results = postgre.db_read(query, user=user_email)

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

def getAllNoCategory(data, user_email):
    try:
        query = """
            SELECT s.id_symptom,
                   s.name,
                   s.synonymous,
                   s.status,
                   s.link,
                   s.hpo_id,
                   s.external_id
            FROM symptoms s
            LEFT JOIN categories_symptoms cs ON s.id_symptom = cs.id_symptom
            WHERE cs.id_symptom IS NULL
            ORDER BY s.name ASC
        """
        results = postgre.db_read(query, user=user_email)

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
        print("error getAllNoCategory", e)
        return False


def getByWord(data, user_email):
    try:
    
        palabra = data.get("palabra", "").strip()
        
        if not palabra:
            return []  # Si está vacío, devolvemos lista vacía en vez de todo
    
        query = """
            SELECT * 
            FROM symptoms 
            WHERE name ILIKE %s 
               OR synonymous ILIKE %s
        """

        like_pattern = f"%{palabra}%"  
        
        results = postgre.db_read(query, params=(like_pattern, like_pattern), user=user_email)
        
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
        print("error getByWord", e)
        return False

def getByCode(data, user_email):
    try:
    
        hpo_id = data.get("hpo_id", "").strip()
        
        if not hpo_id:
            return []  # Si está vacío, devolvemos lista vacía en vez de todo
    
        query = """
            SELECT * 
            FROM symptoms 
            WHERE COALESCE(hpo_id::TEXT, '') ILIKE %s 
        """

        like_pattern = f"%{hpo_id}%"  
        
        results = postgre.db_read(query, params=(like_pattern, ), user=user_email)
        
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
        print("error getByCode", e)
        return False

def getOne(data, user_email):
    try:
        sym_id = data.get("id", "")

        # Sintoma principal
        query_sym = "SELECT * FROM symptoms WHERE id_symptom = %s"
        results_sym = postgre.db_read(query_sym, params=(sym_id,), user=user_email)
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
        query_langs = "SELECT * FROM tl_symptoms WHERE id_symptom = %s"
        results_langs = postgre.db_read(query_langs, params=(sym_id,), user=user_email)
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

def createSym(data, user_email):
    try:
        # Datos del síntoma
        name = data.get("name", "")
        hpo_id = data.get("hpo_id", "")
        synonymous = data.get("synonymous", "")
        username = data.get("username", "")

        # Datos de los lenguajes
        languages = data.get("languages", [])

        # Datos de la patología
        pat_id = data.get("pat_id", "").strip()
        important = data.get("important", "")
        frecuency = data.get("frecuency", "")
        link = data.get("link", "")

        # Generar código RDC automáticamente si hpo_id está vacío
        if not hpo_id:
            query = """
                SELECT hpo_id
                FROM Symptoms
                WHERE hpo_id LIKE 'RDC_%'
                ORDER BY CAST(SUBSTRING(hpo_id FROM 5) AS INTEGER) DESC
                LIMIT 1
            """
            ultimo_rdc = postgre.db_read(query, user=user_email)

            if ultimo_rdc and len(ultimo_rdc) > 0 and ultimo_rdc[0][0]:
                numero = int(ultimo_rdc[0][0].split('_')[1]) + 1
            else:
                numero = 1

            hpo_id = f"RDC_{str(numero).zfill(6)}"

        # Crear el síntoma
        query = """
            INSERT INTO Symptoms (name, external_id, hpo_id, synonymous, status)
            VALUES (
                %s,
                (SELECT 'SYM_' || LPAD(CAST(COALESCE(MAX(CAST(SUBSTRING(external_id FROM 5) AS INTEGER)), 0) + 1 AS TEXT), 6, '0')
                 FROM Symptoms),
                %s, %s, 'pending'
            )
            RETURNING id_symptom;
        """
        sym_id = postgre.db_insert(query, params=(name, hpo_id, synonymous), user=user_email)

        if not sym_id:
            return False  # No se pudo crear el síntoma

        # Crear las traducciones del síntoma
        for lang in languages:
            query = """
                INSERT INTO tl_symptoms (id_symptom, language, value, status)
                VALUES (%s, %s, %s, 'pending')
            """
            postgre.db_insert(query, params=(sym_id, lang["language"], lang["value"]), user=user_email)

        # Si hay una patología asociada, insertar en pathologies_symptoms
        if pat_id:
            query = """
                INSERT INTO pathologies_symptoms (id_pathology, id_symptom, status, link, importante, frequency)
                VALUES (%s, %s, 'pending', %s, %s, %s)
            """
            postgre.db_insert(query, params=(pat_id, sym_id, link, str(important), frecuency), user=user_email)

        return True

    except Exception as e:
        print("Error en createSym:", str(e))
        return False
    
def updateSym(data, user_email):
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
        languages = data.get("languages", [])
        
        #Datos de la patologia
        pat_id = data.get("pat_id", "")
        important = data.get("important", "")
        frecuency = data.get("frecuency", "")
        link = data.get("link", "")
        
        # 1. Update principal
        query_update = """
            UPDATE symptoms
            SET name = %s,
                hpo_id = %s,
                synonymous = %s,
                status = %s
            WHERE id_symptom = %s
        """

        postgre.db_insert(query_update, params=(name, hpo_id, synonymous, state, sym_id), user=user_email)

        # 2. Actualizar idiomas (borrar e insertar)
        query_delete_lang = "DELETE FROM tl_symptoms WHERE id_symptom = %s"
        postgre.db_insert(query_delete_lang, params=(sym_id,), user=user_email)
        for lang in languages:
            query_lang = """
                INSERT INTO tl_symptoms (id_symptom, language, value, status)
                VALUES (%s, %s, %s, 'pending')
            """
            postgre.db_insert(query_lang, params=(sym_id, lang["language"], lang["value"]), user=user_email)

        return sym_id

    except Exception as e:
        print("error updatePat", e)
        return False
    
def validateSymFirst(data, user_email):
    try:
 
        sym_id = data.get("sym_id", "")
        
        query = "UPDATE symptoms SET status = 'verified' WHERE id_symptom = %s"
        result = postgre.db_insert(query, params=(sym_id,), user=user_email)
        return True if result else False
    except Exception as e:
        print("error validateSymFirst", e)
        return False
    
def validateSymSecond(data, user_email):
    try:
 
        sym_id = data.get("sym_id", "")
        
        query = "UPDATE symptoms SET status = 'active' WHERE id_symptom = %s"
        result = postgre.db_insert(query, params=(sym_id,), user=user_email)
        return True if result else False
    except Exception as e:
        print("error validateSymSecond", e)
        return False
    
def deleteSym(data, user_email):
    try:
        sym_id = data.get("id","")
        
        # 1. Borro idiomas
        query_delete_lang = "DELETE FROM tl_symptoms WHERE id_symptom = %s"
        postgre.db_insert(query_delete_lang, params=(sym_id,), user=user_email)
            
        # 3. Borro relaciones patologia-sintoma (ESTO VER CON SALI!!!!!!!!!!)
        query_delete_relations = "DELETE FROM pathologies_symptoms WHERE id_symptom = %s"
        postgre.db_insert(query_delete_relations, params=(sym_id,), user=user_email)
        
        # 4. Borro relaciones categoria-sintoma (ESTO VER CON SALI!!!!!!!!!!)
        query_delete_relationscategories = "DELETE FROM categories_symptoms WHERE id_symptom = %s"
        postgre.db_insert(query_delete_relationscategories, params=(sym_id,), user=user_email)
        
        # 5. Borro el sintoma principal
        query_delete_sym = "DELETE FROM symptoms WHERE id_symptom = %s"
        postgre.db_insert(query_delete_sym, params=(sym_id,), user=user_email)
        
        return True

    except Exception as e:
        print("error deletePat", e)
        return False

def getPendingRelations(data, user_email):
    try:
        query = """
            SELECT 
                ps.id_pathology, 
                p.name AS nombre_patologia, 
                s.id_symptom, 
                s.hpo_id, 
                s.name AS nombre_sintoma,
                ps.link, 
                ps.importante, 
                ps.frequency
            FROM pathologies_symptoms ps
            JOIN pathologies p ON ps.id_pathology = p.id_pathology
            JOIN symptoms s ON ps.id_symptom = s.id_symptom
            WHERE ps.status = 'pending'
            ORDER BY p.name ASC
        """

        results = postgre.db_read(query, user=user_email)

        output = [{
            "pat_id": row[0],
            "pat_name": row[1],
            "sym_id": row[2],
            "sym_hpo": row[3],
            "sym_name": row[4],
            "link": row[5],
            "important": row[6],
            "frequency": row[7]
        } for row in results]

        return output

    except Exception as e:
        print("error getPendingRelations", e)
        return False

def validateRelation(data, user_email):
    try:
        pat_id = data.get("pat_id")
        sym_id = data.get("sym_id")
        query = """
            UPDATE pathologies_symptoms
            SET status = 'verified'
            WHERE id_pathology = %s AND id_symptom = %s
        """
        result = postgre.db_insert(query, params=(pat_id, sym_id), user=user_email)
        return result
    except Exception as e:
        print("error validateRelation", e)
        return False

def deleteRelation(data, user_email):
    try:
        pat_id = data.get("pat_id")
        sym_id = data.get("sym_id")
        query = """
            DELETE FROM pathologies_symptoms
            WHERE id_pathology = %s AND id_symptom = %s
        """
        result = postgre.db_insert(query, params=(pat_id, sym_id), user=user_email)
        return True if result else False
    except Exception as e:
        print("error deleteRelation", e)
        return False
    
def createRelation(data, user_email):
    try:
        pat_id = data.get("pat_id")
        sym_id = data.get("sym_id")
        state = data.get("state")

        link = data.get('link', '')
        important = bool(data.get('important', False))
        frequency = data.get('frequency', '')

        query = """
            INSERT INTO pathologies_symptoms 
                (id_pathology, id_symptom, status, link, importante, frequency)
            VALUES (%s, %s, 'pending', %s, %s, %s)
        """
        result = postgre.db_insert(query, params = (pat_id, sym_id, link, important, frequency), user=user_email)

        return True if result else False
    except Exception as e:
        print("error createRelation", e)
        return False
    
def updateRelation(data, user_email):
    try:
        pat_id = data.get("pat_id")
        sym_id = data.get("sym_id")

        link = data.get("link", "")
        important = data.get("important", None)
        frequency = data.get("frequency", None)

        query = """
            UPDATE pathologies_symptoms
            SET link = %s,
                importante = %s,
                frequency = %s
            WHERE id_pathology = %s
              AND id_symptom = %s
        """
        result = postgre.db_insert(
            query,
            params=(link, important, frequency, pat_id, sym_id),
            user=user_email
        )

        return result
    except Exception as e:
        print("error updateRelation:", e)
        return False
    
def getRelation(data, user_email):
    try:
        pat_id = data.get("pat_id")
        sym_id = data.get("sym_id")
        query = """
            SELECT 
                ps.id_pathology,
                s.name,
                s.synonymous,
                s.id_symptom,
                s.hpo_id,
                ps.status,
                ps.link,
                ps.importante,
                ps.frequency
            FROM pathologies_symptoms ps
            INNER JOIN symptoms s ON ps.id_symptom = s.id_symptom
            WHERE ps.id_pathology = %s 
              AND ps.id_symptom = %s
            ORDER BY ps.status DESC, s.name ASC
        """
        
        results = postgre.db_read(query, params=(pat_id, sym_id), user=user_email)

        output = [
            {
                "pat_id": row[0],
                "name": row[1],
                "synonymous": row[2],
                "sym_id": row[3],
                "hpo_id": row[4],
                "state": row[5],
                "link": row[6],
                "important": row[7],
                "frequency": row[8]
            }
            for row in results
        ]

        return output

    except Exception as e:
        print("error getRelation:", e)
        return []