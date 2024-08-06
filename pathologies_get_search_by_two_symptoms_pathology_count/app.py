import json
import postgre

def lambda_handler(event, context):
    sym_id_1 = event['queryStringParameters']['sym_id_1']
    sym_id_2 = event['queryStringParameters']['sym_id_2']

    query = "select COUNT(*) from pathologies where pat_id in ( select pat_id from pathologies_symptoms where sym_id = '"+ sym_id_1 +"' and pat_id in (select pat_id from pathologies_symptoms where sym_id = '"+ sym_id_2 +"'))"
   
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
