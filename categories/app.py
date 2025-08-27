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

        if action == "get_all":   ##trae todas las categorias 
            result = getAll(data) 
                        
        if action == "create_cat":   ##crea una nueva categoria
            result = createCat(data) 
            
        if action == "delete_cat":    ##borra una categoria y datos relacionados 
            result = deleteCat(data)
            
        if action == "update_cat":         ##edita / actualiza datos de una en particular 
            result = updateCat(data) 
            
        if action == "validate_cat":   ## valida una categoria
            result = validateCat(data) 
            
            
        if result is not False and result is not None:
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
        query = "select * from categories where categories.type = 'system' ORDER BY name ASC"
       
        results = postgre.db_read(query)
    
        output = [{
            "cat_id": row[0],
            "name": row[1],
            "type": row[2],
            "state": row[3],
            "external_id": row[4]
        } for row in results]

        return output
    except Exception as e:
        print("error getAll", e)
        return False
    
def createCat(data):
    try:
        # Extraer datos
        name = data.get("name", "")
        type = data.get("type", "")
        state = data.get("state", "")
        username = data.get("username", "")
        languages = data.get("languages", [])

        query_insert = """
            INSERT INTO categories (name, status, type)
            VALUES (%s, 'pending', %s)
            RETURNING id_category
        """
        cat_id = postgre.db_insert(query_insert, params=(name,type), user=username)

        # Inserto traducciones
        for lang in languages:
            query_lang = """
                INSERT INTO tl_categories (id_category, language, value, status)
                VALUES (%s, %s, %s, 'pending')
            """
            postgre.db_insert(query_lang, params=(cat_id, lang.get("language", ""), lang.get("value", "")), user=username)

        return cat_id

    except Exception as e:
        print("error createCat", e)
        return False
    
def updateCat(data):
    try:
        # Extraer datos
        cat_id = data.get("cat_id")
        name = data.get("name", "")
        type = data.get("type", "")
        state = data.get("state", "")
        username = data.get("username", "")
        languages = data.get("languages", [])

        if not cat_id:
            raise ValueError("Falta id_category para actualizar.")

        # Actualizo categoría principal
        query_update = """
            UPDATE categories
            SET name = %s,
                status = %s,
                type = %s
            WHERE id_category = %s
        """
        postgre.db_update(
            query_update,
            params=(name, state, type, cat_id),
            user=username
        )

        # Borro todas las traducciones existentes
        query_delete = "DELETE FROM tl_categories WHERE id_category = %s"
        postgre.db_update(query_delete, params=(cat_id,), user=username)

        # Inserto las nuevas traducciones
        for lang in languages:
            query_insert_lang = """
                INSERT INTO tl_categories (id_category, language, value, status)
                VALUES (%s, %s, %s, 'pending')
            """
            postgre.db_insert(
                query_insert_lang,
                params=(cat_id, lang.get("language", ""), lang.get("value", "")),
                user=username
            )

        return True

    except Exception as e:
        print("error updateCat", e)
        return False
    
def validateCat(data):
    try:
 
        cat_id = data.get("cat_id", "")
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        query = "UPDATE categories SET status = 'active' WHERE id_category = %s"
        result = postgre.db_insert(query, params=(cat_id,),user=username)
        return result
    except Exception as e:
        print("error validateCat", e)
        return False
    
def deleteCat(data):
    try:
        cat_id = data.get("id","")
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        # 1. Borro idiomas
        query_delete_lang = "DELETE FROM tl_categories WHERE id_category = %s"
        postgre.db_insert(query_delete_lang, params=(cat_id,), user=username)
        
        # 2. Borro relaciones categoria-categoria (ESTO VER CON SALI!!!!!!!!!!)
        query_delete_mother = "DELETE FROM categories_categories WHERE id_category_1 = %s OR id_category_2 = %s"
        postgre.db_insert(query_delete_mother, params=(cat_id, cat_id), user=username)
        
        # 3. Borro la categoria principal
        query_delete_pat = "DELETE FROM categories WHERE id_category = %s"
        postgre.db_insert(query_delete_pat, params=(cat_id,), user=username)
        
        return True

    except Exception as e:
        print("error deleteCat", e)
        return False
