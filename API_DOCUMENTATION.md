# InternTrack API Documentation

Base URL while running locally: `http://127.0.0.1:8000`

Interactive documentation: `/docs`

## General

### `GET /`
Returns the welcome message and documentation paths.

### `GET /health`
Returns `{"status":"ok"}` when the app is running.

## Applications

### `POST /applications`
Creates an application.

Required fields:
- `company` (string, 1–100 characters)
- `role` (string, 1–120 characters)
- `application_date` (`YYYY-MM-DD`)

Optional fields:
- `status`: `Saved`, `Applied`, `Assessment`, `Interview`, `Offer`, or `Rejected` (defaults to `Applied`)
- `job_url` (string or null)
- `notes` (string or null)

Success: `201 Created`, returning the saved record.

### `GET /applications`
Lists applications newest ID first.

Query parameters:
- `status` (optional): filter by allowed status
- `limit` (optional): 1–100, defaults to 50
- `offset` (optional): zero or greater, defaults to 0

Success: `200 OK`, returning a JSON array.

### `GET /applications/{application_id}`
Returns one application.

Errors: `404 Not Found` if the ID does not exist.

### `PATCH /applications/{application_id}`
Updates only the fields supplied in the JSON body. At least one field is required.

Errors:
- `400 Bad Request` if the body is empty
- `404 Not Found` if the ID does not exist
- `422 Unprocessable Entity` if field validation fails

### `DELETE /applications/{application_id}`
Deletes one application.

Success: `204 No Content`.

Error: `404 Not Found` if the ID does not exist.

## Statistics

### `GET /stats`
Returns the total number of applications and counts grouped by status.

Example:

```json
{
  "total": 3,
  "by_status": {
    "Applied": 2,
    "Interview": 1
  }
}
```

## Example `POST /applications` body

```json
{
  "company": "Example Labs",
  "role": "Python Intern",
  "application_date": "2026-10-24",
  "status": "Applied",
  "job_url": "https://example.com/jobs/123",
  "notes": "Applied through the company careers page"
}
```
