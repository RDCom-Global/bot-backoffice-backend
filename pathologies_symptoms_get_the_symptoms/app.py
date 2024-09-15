import json
import postgre

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']

    query = "select pathologies_symptoms.pat_id, symptoms.name, symptoms.synonymous, symptoms.sym_id, symptoms.hpo_id, symptoms.state from (pathologies_symptoms inner join symptoms on pathologies_symptoms.sym_id = symptoms.sym_id) where pathologies_symptoms.pat_id = '"+ id +"' order by symptoms.state ASC, symptoms.name ASC"
    results = postgre.query_postgresql(query)
    
    output = [{"pat_id": row[0],"name": row[1],"synonymous": row[2],"sym_id": row[3],"hpo_id": row[4],"state": row[5]} for row in results]
    
    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
