import json
import postgre

def lambda_handler(event, context):

    query = "SELECT cc.cat_id_1, c1.name AS name_1, cc.cat_id_2, c2.name AS name_2, cc.state FROM categories_categories cc JOIN categories c1 ON cc.cat_id_1 = c1.cat_id JOIN categories c2 ON cc.cat_id_2 = c2.cat_id WHERE cc.state = 'pending'"
    
    results = postgre.query_postgresql(query)
    
    output = [{"cat_id_1": row[0],"name_1": row[1],"cat_id_2": row[2],"name_2": row[3],"state": row[4]} for row in results]

    return {
        "statusCode": 200,
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                   },
        "body": json.dumps(output)
    }
