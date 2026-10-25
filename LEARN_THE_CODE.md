# Understand the code before your interview

Use this as a learning checklist. Do not claim you wrote every line independently if you used AI assistance.

## 1. What is an API?
An API lets one program request data or an action from another program. This project exposes HTTP endpoints such as `GET /applications` and `POST /applications`.

## 2. What is FastAPI?
FastAPI is a Python framework for creating HTTP APIs. It reads route decorators such as `@app.get(...)` and builds interactive documentation at `/docs`.

## 3. What is SQLite?
SQLite stores data in a local database file. This project creates a table named `applications` with columns for company, role, date, status, URL, notes and creation time.

## 4. What do GET, POST, PATCH and DELETE mean?
- GET: read data.
- POST: create a record.
- PATCH: update selected fields.
- DELETE: remove a record.

## 5. What is CRUD?
CRUD means Create, Read, Update and Delete. The application endpoints cover all four operations.

## 6. What is Pydantic validation?
The `ApplicationCreate` and `ApplicationUpdate` models check incoming request data. For example, they limit text lengths and restrict `status` to the allowed choices.

## 7. Why are SQL placeholders used?
Queries use `?` placeholders and pass values separately. This helps avoid unsafe SQL string construction for user-supplied values.

## 8. What is a 404 error?
It means the requested application ID was not found. The API returns a clear `Application not found` message.

## 9. What does `/stats` do?
It uses SQL `COUNT` and `GROUP BY` to calculate how many applications exist and how many have each status.

## 10. What are the limitations?
There is no login or per-user data separation. It is a local demo, not a production-ready multi-user service.

## Practice before the interview
1. Run the app.
2. Create one sample application in `/docs`.
3. List applications and filter by status.
4. Update the status, then delete the record.
5. Explain the database table and one SQL query.
6. Explain one limitation and how you would improve it.

If you cannot explain a section yet, learn it before presenting the project.
