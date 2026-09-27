def validate_task_data(data):
    errors = {}

    if not isinstance(data, dict):
        return {"body": "Request body must be a JSON object"}

    title = data.get("title")

    if title is None:
        errors["title"] = "Title is required"
    elif not isinstance(title, str):
        errors["title"] = "Title must be a string"
    elif not title.strip():
        errors["title"] = "Title cannot be empty"
    elif len(title.strip()) > 100:
        errors["title"] = "Title must not exceed 100 characters"

    description = data.get("description")

    if description is not None:
        if not isinstance(description, str):
            errors["description"] = "Description must be a string"
        elif len(description) > 500:
            errors["description"] = "Description must not exceed 500 characters"

    completed = data.get("completed", False)

    if not isinstance(completed, bool):
        errors["completed"] = "Completed must be a boolean"

    return errors