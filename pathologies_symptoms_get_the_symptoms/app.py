import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']

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
            pathologies_symptoms.id_pathology = '""" + id + """' 
            AND symptoms.status != 'inactive'
        ORDER BY 
            pathologies_symptoms.status DESC, 
            symptoms.name ASC
    """


    results = postgre.query_postgresql(query)
    
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
    
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps(output)
    }