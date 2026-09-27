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
        data = request.get_json()

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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)