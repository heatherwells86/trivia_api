````markdown
# Trivia API

This project is a full-stack trivia application built with Flask, SQLAlchemy, PostgreSQL, and React.

The application allows users to:

- View trivia categories
- View paginated trivia questions
- Search questions
- Filter questions by category
- Add new questions
- Delete questions
- Take quizzes using randomly selected questions
- Prevent previously answered questions from appearing again during a quiz

---

# Project Dependencies

## Backend

The backend uses:

- Python 3
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- SQLAlchemy
- PostgreSQL
- psycopg2

## Frontend

The frontend uses:

- React
- jQuery
- npm

---

# Installation and Setup

## 1. Clone the Project

Clone the project repository and navigate into the project directory.

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
````

---

## 2. Create a Python Virtual Environment

Create a virtual environment from the project directory:

```bash
python3 -m venv venv
```

### Windows

```cmd
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## 3. Install Backend Dependencies

Install the required Python packages:

```bash
pip install flask flask-cors flask-sqlalchemy psycopg2-binary
```

If the project contains a `requirements.txt` file, use:

```bash
pip install -r requirements.txt
```

---

# Database Setup

This project uses PostgreSQL.

The database configuration is located in `models.py`.

The database configuration is:

* Database: `trivia`
* User: `postgres`
* Password: stored in the `DATABASE_PASSWORD` environment variable
* Host: `localhost`
* Port: `5432`

The PostgreSQL password is intentionally not stored directly in the source code.

## Create the PostgreSQL Database

Create the PostgreSQL database before starting the application:

```sql
CREATE DATABASE trivia;
```

The application creates the required tables when the Flask application starts.

## Create the Test Database

The automated tests use a separate PostgreSQL database named `trivia_test`.

Create it before running the tests:

```sql
CREATE DATABASE trivia_test;
```

---

# Configure the Database Password

The application and test suite use the `DATABASE_PASSWORD` environment variable to access PostgreSQL.

## Windows Command Prompt

Open Command Prompt and navigate to the backend directory.

For example:

```cmd
cd C:\Users\YOUR_USERNAME\trivia_api\backend
```

Set the PostgreSQL password:

```cmd
set DATABASE_PASSWORD=YOUR_POSTGRES_PASSWORD
```

Verify that the environment variable is set:

```cmd
echo %DATABASE_PASSWORD%
```

The command should display the password that was entered.

The environment variable applies to the current Command Prompt window. If the window is closed, the variable must be set again in a new Command Prompt window.

---

# Running the Backend

From the project directory, activate the virtual environment and start Flask.

## Windows Command Prompt

Set the database password if it has not already been configured:

```cmd
set DATABASE_PASSWORD=YOUR_POSTGRES_PASSWORD
```

Set the Flask application:

```cmd
set FLASK_APP=flaskr
```

Start the Flask development server:

```cmd
flask run
```

The Flask API will normally be available at:

```text
http://localhost:5000
```

---

# Running the Frontend

Open a second terminal window and navigate to the frontend directory.

Install the frontend dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm start
```

The React application will normally be available at:

```text
http://localhost:3000
```

---

# API Documentation

All API responses are returned as JSON.

Successful responses generally contain:

```json
{
    "success": true
}
```

Error responses contain:

```json
{
    "success": false,
    "error": 404,
    "message": "resource not found"
}
```

---

# GET /categories

Returns all available trivia categories.

## Request Parameters

None.

## Response Body

```json
{
    "success": true,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography"
    }
}
```

The category IDs are used by other endpoints when filtering questions.

---

# GET /questions

Returns a paginated list of trivia questions.

## Request Parameters

| Parameter | Type    | Required | Description                                   |
| --------- | ------- | -------- | --------------------------------------------- |
| `page`    | integer | No       | The page number to retrieve. Defaults to `1`. |

Example:

```text
GET /questions?page=1
```

## Response Body

```json
{
    "success": true,
    "questions": [
        {
            "id": 1,
            "question": "What is the capital of France?",
            "answer": "Paris",
            "category": "6",
            "difficulty": 1
        }
    ],
    "total_questions": 10,
    "categories": {
        "1": "Science",
        "2": "Art",
        "6": "Geography"
    },
    "current_category": null
}
```

The API returns up to 10 questions per page.

If the requested page does not contain any questions, the API returns a successful response with an empty `questions` array.

---

# POST /questions

Creates a new trivia question.

## Request Parameters

The request body must contain:

* `question`
* `answer`
* `category`
* `difficulty`

## Example Request Body

```json
{
    "question": "What is the largest planet in our solar system?",
    "answer": "Jupiter",
    "category": "1",
    "difficulty": 2
}
```

## Response Body

```json
{
    "success": true,
    "created": 11
}
```

The `created` value contains the ID of the newly created question.

## Error Response

If the request body is missing or required fields are missing:

```json
{
    "success": false,
    "error": 422,
    "message": "unprocessable"
}
```

---

# DELETE /questions/<question_id>

Deletes a question using its ID.

## Request Parameters

The question ID is included in the URL.

Example:

```text
DELETE /questions/10
```

## Response Body

```json
{
    "success": true,
    "deleted": 10,
    "questions": [],
    "total_questions": 9
}
```

The response includes the deleted question ID and the updated question list.

## Error Response

If the question does not exist:

```json
{
    "success": false,
    "error": 404,
    "message": "resource not found"
}
```

---

# POST /questions/search

Searches the question database for questions containing the supplied search term.

The search is case-insensitive.

## Request Parameters

The request body must contain:

* `searchTerm`

## Example Request Body

```json
{
    "searchTerm": "capital"
}
```

## Response Body

```json
{
    "success": true,
    "questions": [
        {
            "id": 1,
            "question": "What is the capital of France?",
            "answer": "Paris",
            "category": "6",
            "difficulty": 1
        }
    ],
    "total_questions": 1,
    "current_category": null,
    "categories": {
        "1": "Science",
        "6": "Geography"
    }
}
```

If the search term does not match any questions, the API returns a successful response with an empty `questions` array.

```json
{
    "success": true,
    "questions": [],
    "total_questions": 0,
    "current_category": null,
    "categories": {
        "1": "Science",
        "6": "Geography"
    }
}
```

## Error Response

If `searchTerm` is missing:

```json
{
    "success": false,
    "error": 422,
    "message": "unprocessable"
}
```

---

# GET /categories/<category_id>/questions

Returns questions belonging to a specific category.

## Request Parameters

The category ID is included in the URL.

An optional `page` query parameter can be used for pagination.

Example:

```text
GET /categories/6/questions?page=1
```

## Response Body

```json
{
    "success": true,
    "questions": [
        {
            "id": 1,
            "question": "What is the capital of France?",
            "answer": "Paris",
            "category": "6",
            "difficulty": 1
        }
    ],
    "total_questions": 1,
    "categories": {
        "1": "Science",
        "6": "Geography"
    },
    "current_category": 6
}
```

The `current_category` value identifies the category currently being displayed.

## Error Response

If the category does not exist:

```json
{
    "success": false,
    "error": 404,
    "message": "resource not found"
}
```

---

# POST /quizzes

Returns a random question for a quiz.

The endpoint can return questions from all categories or restrict the questions to a specific category.

Questions listed in `previous_questions` are excluded from the results.

## Request Parameters

The request body may contain:

* `previous_questions`
* `quiz_category`

## Example Request Body

```json
{
    "previous_questions": [1, 4, 7],
    "quiz_category": {
        "id": 6,
        "type": "Geography"
    }
}
```

## Response Body

```json
{
    "success": true,
    "question": {
        "id": 12,
        "question": "What is the capital of Italy?",
        "answer": "Rome",
        "category": "6",
        "difficulty": 1
    }
}
```

The returned question will not have an ID contained in `previous_questions`.

---

# POST /quizzes Without a Category

The API can also return questions from all categories.

## Example Request Body

```json
{
    "previous_questions": [1, 2, 3],
    "quiz_category": {
        "id": null,
        "type": "All"
    }
}
```

## Response Body

```json
{
    "success": true,
    "question": {
        "id": 8,
        "question": "What is the largest ocean?",
        "answer": "Pacific Ocean",
        "category": "5",
        "difficulty": 2
    }
}
```

---

# Quiz With No Questions Remaining

If all questions matching the quiz criteria have already been used, the API returns:

```json
{
    "success": true,
    "question": null
}
```

This allows the frontend to determine that there are no more available questions.

## Error Response

If the request body is invalid or missing:

```json
{
    "success": false,
    "error": 422,
    "message": "unprocessable"
}
```

---

# Error Responses

## 404 Not Found

The API returns a `404` response when a requested resource does not exist.

Examples include:

* Requesting a question that does not exist
* Requesting a category that does not exist
* Requesting an unknown API route

## Response Body

```json
{
    "success": false,
    "error": 404,
    "message": "resource not found"
}
```

---

# 422 Unprocessable Entity

The API returns a `422` response when a request is missing required information or contains invalid request data.

## Response Body

```json
{
    "success": false,
    "error": 422,
    "message": "unprocessable"
}
```

---

# API Endpoint Summary

| Method | Endpoint                              | Description                      |
| ------ | ------------------------------------- | -------------------------------- |
| GET    | `/categories`                         | Returns all categories           |
| GET    | `/questions`                          | Returns paginated questions      |
| POST   | `/questions`                          | Creates a new question           |
| DELETE | `/questions/<question_id>`            | Deletes a question               |
| POST   | `/questions/search`                   | Searches questions               |
| GET    | `/categories/<category_id>/questions` | Returns questions for a category |
| POST   | `/quizzes`                            | Returns a random quiz question   |

---

# Testing

The project includes automated tests for the API using Python's `unittest` framework.

The tests cover:

* Getting categories
* Getting paginated questions
* Invalid pagination
* Deleting questions
* Deleting nonexistent questions
* Creating questions
* Invalid question creation
* Searching questions
* Case-insensitive searches
* Searches with no results
* Invalid searches
* Getting questions by category
* Invalid categories
* Generating quiz questions
* Filtering quiz questions by category
* Excluding previously selected questions
* Handling quizzes with no remaining questions
* Invalid quiz requests
* 404 errors
* 422 errors

## Run the Tests

Make sure the `DATABASE_PASSWORD` environment variable is set before running the tests.

From Windows Command Prompt:

```cmd
set DATABASE_PASSWORD=YOUR_POSTGRES_PASSWORD
```

Then run:

```cmd
python test_flaskr.py
```

The test suite can also be run using unittest discovery:

```cmd
python -m unittest discover
```

The tests use the PostgreSQL database:

```text
trivia_test
```

---

# Project Structure

A typical project structure is:

```text
trivia/
│
├── backend/
│   ├── flaskr/
│   │   └── __init__.py
│   ├── models.py
│   └── test_flaskr.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── stylesheets/
│   │   └── ...
│   ├── package.json
│   └── ...
│
└── README.md
```

---

# Frontend API Integration

The React frontend communicates with the Flask API using AJAX requests.

For example, searching questions uses:

```javascript
$.ajax({
    url: `/questions/search`,
    type: 'POST',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify({
        searchTerm: searchTerm
    })
});
```

The search endpoint uses:

```text
/questions/search
```

rather than:

```text
/questions
```

because the Flask application defines the search operation as a separate POST endpoint.

---

# CORS

CORS is enabled so that the React frontend can communicate with the Flask backend during development.

The Flask application supports the HTTP methods required by the API, including:

```text
GET
POST
DELETE
OPTIONS
```

---

# Database Models

## Question

Each question contains:

```text
id
question
answer
category
difficulty
```

Example:

```json
{
    "id": 1,
    "question": "What is the capital of France?",
    "answer": "Paris",
    "category": "6",
    "difficulty": 1
}
```

## Category

Each category contains:

```text
id
type
```

Example:

```json
{
    "id": 6,
    "type": "Geography"
}
```

---

# Environment Variables

The following environment variable is required for PostgreSQL authentication:

```text
DATABASE_PASSWORD
```

The password should not be committed to the repository.

On Windows Command Prompt:

```cmd
set DATABASE_PASSWORD=YOUR_POSTGRES_PASSWORD
```

---

# Notes

* Questions are displayed 10 at a time.
* Question searches are case-insensitive.
* Quiz questions are selected randomly.
* Previously answered quiz questions are excluded.
* Category filtering uses the category ID stored with each question.
* Invalid requests return a `422` response.
* Missing resources return a `404` response.
* PostgreSQL credentials are stored using environment variables rather than directly in the source code.
* The automated test suite uses a separate `trivia_test` PostgreSQL database.

```
```
