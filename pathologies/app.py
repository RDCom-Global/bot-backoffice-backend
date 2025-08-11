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
            result = getAll(data) ##replace for the correct method
        
        if action == "get_one":
            result = getOne(data) ##replace for the correct method
            
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
        name = data["name"]
        orpha_id = data["orpha_id"]
        omim_id = data["omim_id"]
        type = data["type"]
        username = data["username"]
        mother = data["mother"]
        languages = data["languages"]
        codes = data["codes"]

        # Obtener nuevo pat_id dinámicamente
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

        # Insert madre (si corresponde)
        if mother:
            query_mother = """
                INSERT INTO pathologies_pathologies (pat_id_1, pat_id_2, state, username)
                VALUES (%s, %s, 'pending', %s)
            """
            postgre.db_insert(query_mother, user=username, params=(mother, pat_id, username))

        # Traducciones
        for lang in languages:
            query_lang = """
                INSERT INTO pathologies_translations (pat_id, language, value, state, username)
                VALUES (%s, %s, %s, 'pending', %s)
            """
            postgre.db_insert(query_lang, user=username, params=(pat_id, lang["language"], lang["value"], username))

        # Códigos
        for code in codes:
            query_code = """
                INSERT INTO pathologies_codes (pat_id, code_id, value, name, state, date, username)
                VALUES (%s, %s, %s, %s, 'pending', NOW(), %s)
            """
            postgre.db_insert(query_code, user=username, params=(pat_id, code["code_id"], code["value"], code["name"], username))

        return pat_id

    except Exception as e:
        print("error", e)
        return False
    
def getAll(data):
    try:
        query = """
            SELECT 
                p.pat_id,
                p.name,
                p.orpha_id,
                p.omim_id,
                p.type,
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
            "codes": row[5]
        } for row in results]

        return output
    except Exception as e:
        print("error", e)
        return False
    
def getOne(data):
    try:
        pat_id = data['queryStringParameters']['id']
        query = "SELECT * FROM pathologies WHERE pat_id = %s"
        results = postgre.db_read(query, user="system", params=(pat_id,))

        output = [{"pat_id": row[0], "name": row[1], "orpha_id": row[2], "omim_id": row[3], "type": row[6]} for row in results]
        return output
    except Exception as e:
        print("error", e)
        return False