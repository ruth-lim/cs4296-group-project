import json

def http_function(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object.
    """
    try:
        # Parse the request body
        request_json = request.get_json(silent=True)
        
        if request_json is None:
            return {"error": "No JSON data provided"}, 400
        
        task_type = request_json.get("type")
        
        if task_type == "rest_api":
            name = request_json.get("name", "World")
            return {"message": f"Hello, {name}!"}, 200
            
        elif task_type == "database_query":
            query_id = request_json.get("id", "1")
            fake_db = {
                "1": {"name": "Alice", "role": "Engineer"},
                "2": {"name": "Bob", "role": "Designer"},
                "3": {"name": "Charlie", "role": "Manager"}
            }
            result = fake_db.get(query_id, {"error": "Record not found"})
            return result, 200
            
        else:
            return {"error": f"Invalid request type: {task_type}"}, 400
            
    except Exception as e:
        return {"error": f"Error processing request: {str(e)}"}, 500