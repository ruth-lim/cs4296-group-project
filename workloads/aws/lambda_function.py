def lambda_handler(event, context):
    task_type = event.get("type")

    if task_type == "rest_api":
        name = event.get("name", "World")
        return {
            "statusCode": 200,
            "body": f"Hello, {name}!"
        }

    elif task_type == "database_query":
        query_id = event.get("id", "1")
        fake_database = {
            "1": {"name": "Alice", "role": "Engineer"},
            "2": {"name": "Bob", "role": "Designer"},
            "3": {"name": "Charlie", "role": "Manager"}
        }
        result = fake_database.get(query_id, {"error": "Record not found"})
        return {
            "statusCode": 200,
            "body": result
        }

    else:
        return {
            "statusCode": 400,
            "body": "Invalid request type"
        }