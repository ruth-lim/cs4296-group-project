import azure.functions as func
import logging
import json
import time
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="rest_api_handler")
def rest_api_handler(req: func.HttpRequest) -> func.HttpResponse:
    # Start timing and cold start detection
    start_time = time.time()
    is_cold_start = "FUNCTION_INITIALIZED" not in os.environ
    if is_cold_start:
        os.environ["FUNCTION_INITIALIZED"] = "true"
    
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        req_body = req.get_json()
        task_type = req_body.get('type')
        
        if task_type == "rest_api":
            name = req_body.get('name', 'World')
            result = f"Hello, {name}!"
            response_body = json.dumps({"message": result})
            
        elif task_type == "database_query":
            query_id = req_body.get('id', '1')
            fake_db = {
                "1": {"name": "Alice", "role": "Engineer"},
                "2": {"name": "Bob", "role": "Designer"},
                "3": {"name": "Charlie", "role": "Manager"}
            }
            result = fake_db.get(query_id, {"error": "Record not found"})
            response_body = json.dumps(result)
            
        else:
            response_body = json.dumps({"error": f"Invalid request type: {task_type}"})
            return func.HttpResponse(response_body, mimetype="application/json", status_code=400)
    
    except ValueError:
        response_body = json.dumps({"error": "Invalid JSON input"})
        return func.HttpResponse(response_body, mimetype="application/json", status_code=400)
    except Exception as e:
        response_body = json.dumps({"error": f"Error processing request: {str(e)}"})
        return func.HttpResponse(response_body, mimetype="application/json", status_code=500)
    
    # Calculate execution time
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # in milliseconds
    
    # Log performance data
    logging.info(f"Execution time: {execution_time}ms, Cold start: {is_cold_start}")
    
    return func.HttpResponse(
        response_body,
        mimetype="application/json",
        status_code=200
    )