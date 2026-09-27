# Task CRUD API

A simple RESTful CRUD API built with **Flask**, **SQLAlchemy**, and **SQLite**.

The API manages a single entity: **Task**.

## Features

* Create, read, update, and delete tasks
* SQLite database persistence
* Input validation
* JSON error responses
* HTTP status codes
* Edge-case handling
* Automated tests with pytest

## Task Fields

| Field         | Type    | Required       | Limit               |
| ------------- | ------- | -------------- | ------------------- |
| `id`          | Integer | Auto-generated | —                   |
| `title`       | String  | Yes            | 100 characters      |
| `description` | String  | No             | 500 characters      |
| `completed`   | Boolean | No             | Defaults to `false` |

## API Endpoints

| Method | Endpoint      | Description      |
| ------ | ------------- | ---------------- |
| GET    | `/`           | Check API status |
| POST   | `/tasks`      | Create a task    |
| GET    | `/tasks`      | Get all tasks    |
| GET    | `/tasks/<id>` | Get one task     |
| PUT    | `/tasks/<id>` | Update a task    |
| DELETE | `/tasks/<id>` | Delete a task    |

## Setup

Clone the project and enter the directory:

```bash
git clone <repository-url>
cd task-crud-api
```

Create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

```bash
python app.py
```

The API runs at:

```text
http://127.0.0.1:5000
```

## Example Request

Create a task:

```bash
curl -X POST http://127.0.0.1:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Flask",
    "description": "Practice REST APIs"
  }'
```

Example response:

```json
{
  "id": 1,
  "title": "Learn Flask",
  "description": "Practice REST APIs",
  "completed": false
}
```

## Run Tests

Make sure the virtual environment is active, then run:

```bash
python -m pytest -v
```

The test suite covers CRUD operations, validation, malformed JSON, nonexistent resources, invalid IDs, and unsupported HTTP methods.

## Project Structure

```text
task-crud-api/
├── app.py
├── database.py
├── models.py
├── validators.py
├── requirements.txt
├── tests/
│   └── test_task.py
├── .gitignore
└── README.md
```

## Technologies

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* pytest
