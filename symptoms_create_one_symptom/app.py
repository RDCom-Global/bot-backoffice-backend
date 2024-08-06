import json
import postgre

def lambda_handler(event, context):

    name = event['body']['name']
    sym_id = event['body']['sym_id']
    hpo_id = event['body']['hpo_id']
    synonymous = event['body']['synonymous']
    link = event['body']['link']
    state = event['body']['state']

    query = "insert into Symptoms (name, sym_id, hpo_id, synonymous, link, state) values ('"+ name +"', '"+ sym_id +"', '"+ hpo_id +"', '"+ synonymous +"', '"+ link +"', '"+ state +"') RETURNING *"

    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
