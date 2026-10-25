# InternTrack API

InternTrack is a beginner-friendly REST API for keeping track of internship applications. It uses **Python, FastAPI and SQLite**. It is backend-only; there is no frontend.

## Features

- Create an application
- List applications, optionally filter by status
- Get one application by ID
- Update application details
- Delete an application
- View totals grouped by application status
- Automatic interactive API documentation
- Input validation and clear 404 errors
- SQLite database created automatically on startup

## Tech stack

- Python 3.10+
- FastAPI — API framework
- SQLite — lightweight local database
- Uvicorn — local development server
- Pytest and HTTPX — tests

## Run locally (Windows PowerShell)

1. Install Python 3.10 or newer.
2. Extract this folder and open it in VS Code.
3. Open the VS Code terminal in this folder.
4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run:
   `.\.venv\Scripts\activate.bat`

5. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Start the API:

   ```powershell
   uvicorn main:app --reload
   ```

7. Open `http://127.0.0.1:8000/docs` in your browser. Use the Swagger UI to try the endpoints.

The `interntrack.db` SQLite file is created automatically when the app starts. It is local development data; it is not included in the repository.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/applications` | Create an application |
| GET | `/applications` | List applications |
| GET | `/applications?status=Interview` | Filter by status |
| GET | `/applications/{id}` | Get one application |
| PATCH | `/applications/{id}` | Update selected fields |
| DELETE | `/applications/{id}` | Delete an application |
| GET | `/stats` | Total applications and status counts |

Allowed statuses: `Saved`, `Applied`, `Assessment`, `Interview`, `Offer`, `Rejected`.

## Example request

Send a `POST` request to `/applications` with this JSON body:

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

The API returns the created application, including its generated `id`.

## Run tests

```powershell
pytest -q
```

## Project structure

```text
InternTrack-Backend/
├── main.py
├── requirements.txt
├── README.md
├── API_DOCUMENTATION.md
├── .gitignore
└── tests/
    └── test_api.py
```

## Important limitations

- This starter project has no user accounts or authentication; all local users share the same application list.
- SQLite is suitable for a small demo. A deployed multi-user service would need stronger configuration, authentication, and deployment planning.
- Do not put passwords, API keys, or personal data in the repository.

## Before submitting

- Run the app and try each endpoint in `/docs`.
- Run the tests.
- Read the code and make sure you can explain it.
- Replace this README's example details with your own understanding and screenshots if useful.
- Push the code to a public GitHub repository and verify that the link opens in a private/incognito window.
