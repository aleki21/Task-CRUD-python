from flask import Flask, request

from database import db
from validators import validate_task_data

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from models import Task

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return {"message": "Task API is running"}

    @app.route("/tasks", methods=["POST"])
    def create_task():
        data = request.get_json(silent=True)

        if data is None:
            return {
                "error": "Invalid JSON",
                "message": "Request body must contain valid JSON"
            }, 400

        errors = validate_task_data(data)

        if errors:
            return {
                "error": "Validation failed",
                "details": errors
            }, 400

        task = Task(
            title=data["title"].strip(),
            description=data.get("description"),
            completed=data.get("completed", False)
        )

        db.session.add(task)
        db.session.commit()

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }, 201

    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        tasks = Task.query.all()

        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
            for task in tasks
        ], 200

    @app.route("/tasks/<int:task_id>", methods=["GET"])
    def get_task(task_id):
        task = db.session.get(Task, task_id)

        if task is None:
            return {
                "error": "Task not found"
            }, 404

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }, 200

    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):
        task = db.session.get(Task, task_id)

        if task is None:
            return {
                "error": "Task not found"
            }, 404

        data = request.get_json(silent=True)

        if data is None:
            return {
                "error": "Invalid JSON",
                "message": "Request body must contain valid JSON"
            }, 400

        errors = validate_task_data(data)

        if errors:
            return {
                "error": "Validation failed",
                "details": errors
            }, 400

        task.title = data["title"].strip()
        task.description = data.get("description")
        task.completed = data.get("completed", False)

        db.session.commit()

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }, 200

    @app.errorhandler(404)
    def handle_not_found(error):
        return {
            "error": "Not found",
            "message": "The requested resource does not exist"
        }, 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)