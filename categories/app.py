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
            
        if action == "get_all_system":   ##trae todas las categorias system
            result = getAllSystem(data) 
            
        if action == "get_one":   ##trae datos con idiomas de una categoria en particular
            result = getOne(data) 
                        
        if action == "create_cat":   ##crea una nueva categoria y sus idiomas
            result = createCat(data) 
            
        if action == "delete_cat":    ##borra una categoria y datos relacionados 
            result = deleteCat(data)
            
        if action == "update_cat":     ##edita / actualiza datos de una en particular 
            result = updateCat(data) 
            
        if action == "validate_cat":   ## valida una categoria
            result = validateCat(data) 
            
        if action == "get_by_word":   ##trae todos las categorias que incluyan una palabra
            result = getByWord(data) 
            
        if action == "get_category_childrens":   ##trae las categorias hijas de una categoria en particular
            result = getCatChild(data) 
            
        if action == "get_categories_of_symptom":   ##trae las categorias para un sintoma determinado
            result = getCatOfSym(data)             
            
        if action == "add_category_to_symptom":   ##agrega una categoria a un sintoma
            result = addCatToSym(data)      
            
        if action == "delete_category_of_symptom":   ##borra una categoria de un sintoma
            result = deleteCatOfSym(data)    

        if action == "get_all_cat_cat":    ##trae todas las relaciones categoria de categoria 
            result = getAllCatCat(data)
            
        if action == "delete_cat_cat":    ##borra una relacion categoria de categoria 
            result = deleteCatCat(data)
            
        if action == "create_cat_cat":    ##crea una relacion categoria de categoria 
            result = createCatCat(data)
            
        if action == "validate_cat_cat":    ##valida una relacion categoria de categoria 
            result = validateCatCat(data)
            
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
        query = "select * from categories ORDER BY name ASC"
       
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
    
def getAllSystem(data):
    try:
        query = "select * from categories where type = 'system' ORDER BY name ASC"
       
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

def getOne(data):
    try:
        cat_id = data.get("id", "")

        # Sintoma principal
        query_cat = "SELECT * FROM categories WHERE id_category = %s"
        results_cat = postgre.db_read(query_cat, params=(cat_id,), user="system")
        category = [{
            "cat_id": row[0],
            "name": row[1],
            "type": row[2],
            "state": row[3],
            "external_id": row[4]
        } for row in results_cat]

        # Idiomas
        query_langs = "SELECT * FROM tl_categories WHERE id_category = %s"
        results_langs = postgre.db_read(query_langs, params=(cat_id,), user="system")
        idiomas = [{
            "cat_id": row[0],
            "language": row[1],
            "value": row[2],
            "state": row[3]
        } for row in results_langs]

        # Devolvemos todo en un solo JSON
        return {
            "category": category,
            "idiomas": idiomas
        }

    except Exception as e:
        print("error getOne", e)
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
        postgre.db_insert(
            query_update,
            params=(name, state, type, cat_id),
            user=username
        )

        # Borro todas las traducciones existentes
        query_delete = "DELETE FROM tl_categories WHERE id_category = %s"
        postgre.db_insert(query_delete, params=(cat_id,), user=username)

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

def getByWord(data):
    try:
        palabra = data.get("palabra", "").strip()
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        query = "SELECT * FROM categories WHERE name ILIKE %s"
        
        results = postgre.db_read(query, params=(f"%{palabra}%",), user=username)
    
        output = [{
            "cat_id": row[0],
            "name": row[1],
            "type": row[2],
            "state": row[3],
            "external_id": row[4]
        } for row in results]

        return output
    except Exception as e:
        print("error getByWord", e)
        return False
    
def getCatChild(data):
    try:
        cat_id = data.get("cat_id", "")
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        query = """
            SELECT 
                cc.id_category_1, 
                cc.id_category_2 AS cat_id, 
                c.name, 
                c.type
            FROM categories_categories cc
            INNER JOIN categories c ON cc.id_category_2 = c.id_category
            WHERE cc.id_category_1 = %s
            ORDER BY c.name ASC
        """
        results = postgre.db_read(query, params=(cat_id,), user=username)

        output = [{"cat_id_1": row[0],"cat_id_2": row[1],"name": row[2],"type": row[3]} for row in results]
       
        return output
    except Exception as e:
        print("error getCatChild", e)
        return False    
    
def getCatOfSym(data):
    try:
        sym_id = data.get("id", "")
        username = data.get('username', 'system')  # o el usuario que corresponda
        query = """
            SELECT 
                categories_symptoms.id_category, 
                categories_symptoms.id_symptom, 
                categories.name, 
                categories.type
            FROM categories_symptoms 
            INNER JOIN categories 
                ON categories_symptoms.id_category = categories.id_category
            WHERE categories_symptoms.id_symptom = %s
            ORDER BY categories.name ASC
        """

        results = postgre.db_read(query, params=(sym_id,), user=username)

        output = [
            {
                "cat_id": row[0],
                "sym_id": row[1],
                "name": row[2],
                "type": row[3]
            }
            for row in results
        ]
    
        return output
    except Exception as e:
        print("error getCatOfSym", e)
        return False   

def deleteCatOfSym(data):
    try:
 
        cat_id = data.get("cat_id", "")
        sym_id = data.get("sym_id", "")
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        query = "DELETE FROM categories_symptoms WHERE id_category = %s AND id_symptom = %s"
        
        result = postgre.db_insert(query, params=(cat_id,sym_id),user=username)
        
        return result
    except Exception as e:
        print("error deleteCatOfSym", e)
        return False
    
def addCatToSym(data):
    try:
        
        cat_id = data.get("cat_id", "")
        sym_id = data.get("sym_id", "")
        state = data.get('state', 'pending')  # opcional, por defecto 'pending'
        username = data.get('username', 'system')  # o el usuario que corresponda

        # Insertamos la relación en la tabla categories_symptoms
        query = """
            INSERT INTO categories_symptoms (id_category, id_symptom, status)
            VALUES (%s, %s, %s)
        """
        result = postgre.db_insert(query, params=(cat_id,sym_id, state),user=username)
        
        return result
    except Exception as e:
        print("error addCatToSym", e)
        return False

def getAllCatCat(data):
    try:

        query = """
            SELECT 
                cc.id_category_1,
                c1.name AS name_1,
                cc.id_category_2,
                c2.name AS name_2,
                cc.status
            FROM categories_categories cc
            JOIN categories c1 ON cc.id_category_1 = c1.id_category
            JOIN categories c2 ON cc.id_category_2 = c2.id_category
            ORDER BY name_1 ASC;
        """
        results = postgre.db_read(query)
        
        output = [{"cat_id_1": row[0],"name_1": row[1],"cat_id_2": row[2],"name_2": row[3],"state": row[4]} for row in results]

        return output
    except Exception as e:
        print("error getAllCatCat", e)
        return False

def deleteCatCat(data):
    try:
 
        cat_id_1 = data.get("cat_id_1", "")
        cat_id_2 = data.get("cat_id_2", "")
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        query = "delete from categories_categories where (id_category_1 = %s AND id_category_2= %s)"
    
        result = postgre.db_insert(query, params=(cat_id_1,cat_id_2),user=username)
        
        return result
    except Exception as e:
        print("error deleteCatCat", e)
        return False
    
def createCatCat(data):
    try:
 
        cat_id_1 = data.get("cat_id_1", "")
        cat_id_2 = data.get("cat_id_2", "")
        username = data.get('username', 'system')  # o el usuario que corresponda
        
        state = data.get('state', 'pending')  # opcional, por defecto 'pending'

        # Insertamos la relación en la tabla categories_categories
        query = """
            INSERT INTO categories_categories (id_category_1, id_category_2, status)
            VALUES (%s, %s, %s)
        """
        result = postgre.db_insert(query, params=(cat_id_1,cat_id_2, state),user=username)
        
        return result
    except Exception as e:
        print("error deleteCatCat", e)
        return False
    
def validateCatCat(data):
    try:
        cat_id_1 = data.get("cat_id_1", "")
        cat_id_2 = data.get("cat_id_2", "")
        username = data.get("username", "system")  
        state = data.get("state", "active")  

        # Update del estado de la relación
        query = """
            UPDATE categories_categories
            SET status = %s
            WHERE id_category_1 = %s AND id_category_2 = %s
        """
        result = postgre.db_insert(
            query,
            params=(state, cat_id_1, cat_id_2),
            user=username
        )

        return result
    except Exception as e:
        print("error validateCatCat", e)
        return False