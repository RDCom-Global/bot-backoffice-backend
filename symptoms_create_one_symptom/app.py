import json
import postgre

def lambda_handler(event, context):

    username = event['queryStringParameters']['username']

    body = json.loads(event['body'])
    
    if 'sym_id' in event['body']:
        name = body['name']
        # sym_id = body['sym_id']
        hpo_id = body.get('hpo_id', '')
        synonymous = body.get('synonymous', '')
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
