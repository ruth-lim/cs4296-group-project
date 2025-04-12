import json

def lambda_handler(event, context):
    try:
        # If coming from Function URL or API Gateway, parse the "body" field
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        task_type = body.get("type")

        if task_type == "rest_api":
            name = body.get("name", "World")
            return {
                "statusCode": 200,
                "body": f"Hello, {name}!"
            }

        elif task_type == "database_query":
            query_id = body.get("id", "1")
            fake_db = {
                "1": {"name": "Alice", "role": "Engineer"},
                "2": {"name": "Bob", "role": "Designer"},
                "3": {"name": "Charlie", "role": "Manager"}
            }
            result = fake_db.get(query_id, {"error": "Record not found"})
            return {
                "statusCode": 200,
                "body": result
            }

        else:
            return {
                "statusCode": 400,
                "body": f"Invalid request type: {task_type}"
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error parsing input: {str(e)}"
        }