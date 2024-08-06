import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']
    name = event['body']['name']
    sym_id = event['body']['sym_id']
    hpo_id = event['body']['hpo_id']
    synonymous = event['body']['synonymous']
    link = event['body']['link']
    state = event['body']['state']

    query = "update symptoms set name = '"+ name +"', sym_id = '"+ sym_id +"', hpo_id = '"+ hpo_id +"', synonymous = '"+ synonymous +"', link = '"+ link +"', state = '"+ state +"' where sym_id = '"+ id +"' RETURNING *"

    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
