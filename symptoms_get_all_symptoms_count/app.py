import json
import postgre

def lambda_handler(event, context):
<<<<<<< HEAD
        query = "select COUNT(*) from symptoms"

=======
    
    query = "select * from symptoms where state='pendiente de verificar'"
>>>>>>> ba363feff47f235e8466f1cff5db82bbc74919a7
    results = postgre.query_postgresql(query)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
