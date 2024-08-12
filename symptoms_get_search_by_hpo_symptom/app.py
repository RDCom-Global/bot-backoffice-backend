import json
import postgre

def lambda_handler(event, context):
    palabra = event['queryStringParameters']['palabra']
<<<<<<< HEAD
    query = "select * from symptoms where hpo_id = '"+ palabra +"' "
    
=======

    query = "select * from symptoms where name ilike '%'|| '"+ palabra +"' ||'%'"
>>>>>>> ba363feff47f235e8466f1cff5db82bbc74919a7
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
