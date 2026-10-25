from contextlib import asynccontextmanager
from datetime import date, datetime, timezone
from typing import Literal

import sqlite3
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, EmailStr, Field

DATABASE_PATH = "interntrack.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                application_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Applied',
                job_url TEXT,
                notes TEXT,
                created_at TEXT NOT NULL
            )
        """)

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(
    title="InternTrack API",
    description="A beginner-friendly REST API for tracking internship applications.",
    version="1.0.0",
    lifespan=lifespan,
)

ApplicationStatus = Literal["Saved", "Applied", "Assessment", "Interview", "Offer", "Rejected"]

class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=120)
    application_date: date
    status: ApplicationStatus = "Applied"
    job_url: str | None = Field(default=None, max_length=500)
    notes: str | None = Field(default=None, max_length=2000)

class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=100)
    role: str | None = Field(default=None, min_length=1, max_length=120)
    application_date: date | None = None
    status: ApplicationStatus | None = None
    job_url: str | None = Field(default=None, max_length=500)
    notes: str | None = Field(default=None, max_length=2000)

class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    company: str
    role: str
    application_date: date
    status: str
    job_url: str | None
    notes: str | None
    created_at: datetime

def row_to_application(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "company": row["company"],
        "role": row["role"],
        "application_date": row["application_date"],
        "status": row["status"],
        "job_url": row["job_url"],
        "notes": row["notes"],
        "created_at": row["created_at"],
    }

@app.get("/", tags=["General"])
def root():
    return {
        "message": "Welcome to InternTrack API",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health", tags=["General"])
def health_check():
    return {"status": "ok"}

@app.post("/applications", response_model=ApplicationOut, status_code=201, tags=["Applications"])
def create_application(application: ApplicationCreate):
    created_at = datetime.now(timezone.utc).isoformat()
    with get_connection() as connection:
        cursor = connection.execute(
            """INSERT INTO applications
               (company, role, application_date, status, job_url, notes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                application.company.strip(),
                application.role.strip(),
                application.application_date.isoformat(),
                application.status,
                application.job_url,
                application.notes,
                created_at,
            ),
        )
        row = connection.execute(
            "SELECT * FROM applications WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return row_to_application(row)

@app.get("/applications", response_model=list[ApplicationOut], tags=["Applications"])
def list_applications(
    status: ApplicationStatus | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    with get_connection() as connection:
        if status:
            rows = connection.execute(
                """SELECT * FROM applications WHERE status = ?
                   ORDER BY id DESC LIMIT ? OFFSET ?""",
                (status, limit, offset),
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM applications ORDER BY id DESC LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()
    return [row_to_application(row) for row in rows]

@app.get("/applications/{application_id}", response_model=ApplicationOut, tags=["Applications"])
def get_application(application_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM applications WHERE id = ?", (application_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return row_to_application(row)

@app.patch("/applications/{application_id}", response_model=ApplicationOut, tags=["Applications"])
def update_application(application_id: int, updates: ApplicationUpdate):
    changes = updates.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="Provide at least one field to update")

    if "application_date" in changes and changes["application_date"] is not None:
        changes["application_date"] = changes["application_date"].isoformat()

    for key in ("company", "role"):
        if key in changes and changes[key] is not None:
            changes[key] = changes[key].strip()

    allowed_columns = {"company", "role", "application_date", "status", "job_url", "notes"}
    if not set(changes).issubset(allowed_columns):
        raise HTTPException(status_code=400, detail="Invalid field")

    with get_connection() as connection:
        existing = connection.execute(
            "SELECT * FROM applications WHERE id = ?", (application_id,)
        ).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Application not found")

        assignments = ", ".join(f"{column} = ?" for column in changes)
        values = list(changes.values()) + [application_id]
        connection.execute(
            f"UPDATE applications SET {assignments} WHERE id = ?", values
        )
        updated = connection.execute(
            "SELECT * FROM applications WHERE id = ?", (application_id,)
        ).fetchone()
    return row_to_application(updated)

@app.delete("/applications/{application_id}", status_code=204, tags=["Applications"])
def delete_application(application_id: int):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM applications WHERE id = ?", (application_id,)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Application not found")
    return None

@app.get("/stats", tags=["Applications"])
def application_stats():
    with get_connection() as connection:
        total = connection.execute(
            "SELECT COUNT(*) AS count FROM applications"
        ).fetchone()["count"]
        rows = connection.execute(
            "SELECT status, COUNT(*) AS count FROM applications GROUP BY status"
        ).fetchall()
    return {
        "total": total,
        "by_status": {row["status"]: row["count"] for row in rows},
    }
