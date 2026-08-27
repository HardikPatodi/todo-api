# To-Do List REST API

A RESTful To-Do List API built with **FastAPI** and **SQLite**.

## Features

-   FastAPI REST API
-   SQLite database
-   CRUD operations for tasks
-   Pydantic request and response models
-   Empty-title validation
-   Proper HTTP status codes: 200, 201, 404 and 422
-   404 handling for non-existent tasks
-   CORS enabled for frontend integration
-   Interactive Swagger documentation
-   Python API test script
-   Feature-based Git workflow

## Project Structure

``` text
To-Do list/
├── tests/
│   └── test_api.py
├── database.py
├── init_db.py
├── main.py
├── models.py
├── requirements.txt
├── README.md
└── tasks.db
```

## Database

SQLite is used for persistent task storage.

The `tasks` table contains:

  Column           Description
  ---------------- ------------------------------
  `id`             Auto-generated task ID
  `title`          Task title
  `description`    Task description
  `completed`      Whether the task is complete
  `created_date`   Task creation date/time

`init_db.py` initializes the database, while `database.py` contains the
CRUD database operations.

## API Endpoints

### GET `/tasks`

Returns all tasks.

**Status:** `200 OK`

### POST `/tasks`

Creates a new task.

**Status:** `201 Created`

Example request:

``` json
{
  "title": "Complete assignment",
  "description": "Finish Assignment 4"
}
```

### PUT `/tasks/{id}`

Updates an existing task, including changing its completion status.

**Status:** `200 OK`

Example request:

``` json
{
  "title": "Complete assignment",
  "description": "Assignment 4 completed",
  "completed": true
}
```

The original `created_date` is preserved when a task is updated.

### DELETE `/tasks/{id}`

Deletes an existing task.

**Status:** `200 OK`

## Validation and Error Handling

  Situation                         Status
  ------------------------------- --------
  Successful GET                     `200`
  Successful PUT                     `200`
  Successful DELETE                  `200`
  Successful POST                    `201`
  Task does not exist                `404`
  Invalid request / empty title      `422`

An empty title is rejected by Pydantic validation because the title has
a minimum length of one character.

Example:

``` json
{
  "title": "",
  "description": "Invalid task"
}
```

returns `422 Unprocessable Entity`.

Requests for a non-existent task ID return `404 Not Found` instead of
crashing the application.

## CORS

CORS is enabled so a browser-based frontend can call the API. This will
be used by Assignment 5.

## Installation

### 1. Create a virtual environment

Windows PowerShell:

``` powershell
python -m venv venv
.env\Scripts\Activate.ps1
```

### 2. Install dependencies

``` powershell
python -m pip install -r requirements.txt
```

## Initialize the Database

``` powershell
python init_db.py
```

This creates the SQLite database and `tasks` table if they do not
already exist.

## Run the API

``` powershell
python -m uvicorn main:app --reload
```

The API will normally run at:

`http://127.0.0.1:8000`

## Interactive Documentation

FastAPI automatically generates Swagger UI.

Open:

`http://127.0.0.1:8000/docs`

You can test all four endpoints directly from the browser.

## Testing

The API test script is located at:

`tests/test_api.py`

Start the API first, then run:

``` powershell
python tests/test_api.py
```

The test script exercises:

1.  GET `/tasks`
2.  POST `/tasks`
3.  PUT `/tasks/{id}`
4.  DELETE `/tasks/{id}`
5.  Empty-title validation
6.  Non-existent task handling

The script prints the HTTP status code and response for each test.

## Manual Swagger Testing

Recommended order:

1.  Run the API.
2.  Open `/docs`.
3.  Test `GET /tasks`.
4.  Test `POST /tasks` with a valid task.
5.  Use the returned ID for `PUT /tasks/{id}`.
6.  Set `completed` to `true` to test completion.
7.  Test `DELETE /tasks/{id}`.
8.  Verify the task is gone with `GET /tasks`.
9.  Test an empty title and a non-existent ID.

## Git Workflow

Endpoint development used separate feature branches:

``` text
feature/get-tasks
feature/post-tasks
feature/put-tasks
feature/delete-tasks
```

Each endpoint was committed separately and merged into `main`.

After confirming the final working version, create a release tag:

``` powershell
git tag v1.0.0
git push origin v1.0.0
```

