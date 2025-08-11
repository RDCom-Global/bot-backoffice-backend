import json
import postgre

def lambda_handler(event, context):
    try:
        query = """
            SELECT 
                p.pat_id,
                p.name,
                p.orpha_id,
                p.omim_id,
                p.type,
                COALESCE(
                    STRING_AGG(pc.code_id || ':' || pc.value, ', '), ''
                ) AS codes
            FROM pathologies p
            LEFT JOIN pathologies_codes pc 
                ON p.pat_id = pc.pat_id AND pc.state != 'inactive'
            WHERE p.state = 'pending'
            GROUP BY p.pat_id, p.name, p.orpha_id, p.omim_id, p.type
            ORDER BY p.name ASC;
        """

        results = postgre.query_postgresql(query)

        output = [{
            "pat_id": row[0],
            "name": row[1],
            "orpha_id": row[2],
            "omim_id": row[3],
            "type": row[4],
            "codes": row[5]
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

    except Exception as e:
        print("Error en lambda_handler:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }