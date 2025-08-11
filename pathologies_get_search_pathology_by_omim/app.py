import json
import postgre

def lambda_handler(event, context):
    palabra = event['queryStringParameters']['palabra']

    query = f"""
        SELECT 
            p.pat_id,
            p.name,
            p.orpha_id,
            p.omim_id,
            COALESCE(STRING_AGG(pc.code_id || ':' || pc.value, ', '), '') AS codes
        FROM pathologies p
        LEFT JOIN pathologies_codes pc 
            ON p.pat_id = pc.pat_id AND pc.state != 'inactive'
        WHERE 
            p.omim_id ILIKE '%{palabra}%' OR
            pc.code_id ILIKE '%{palabra}%' OR
            pc.value ILIKE '%{palabra}%'
        GROUP BY p.pat_id, p.name, p.orpha_id, p.omim_id
        ORDER BY p.name ASC
    """

    results = postgre.query_postgresql(query)

    output = [{
        "pat_id": row[0],
        "name": row[1],
        "orpha_id": row[2],
        "omim_id": row[3],
        "codes": row[4]
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