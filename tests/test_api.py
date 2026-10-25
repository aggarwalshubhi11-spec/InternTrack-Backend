from datetime import date
import os
import tempfile

import main
from fastapi.testclient import TestClient

# Use a separate database for testing.
TEST_DB = os.path.join(tempfile.gettempdir(), "interntrack_test.db")

main.DATABASE_PATH = TEST_DB

# Initialise the database tables before running tests.
with TestClient(main.app) as client:
    pass

client = TestClient(main.app)


def setup_function():
    with main.get_connection() as connection:
        connection.execute("DELETE FROM applications")


def sample_payload():
    return {
        "company": "Example Labs",
        "role": "Python Intern",
        "application_date": str(date.today()),
        "status": "Applied",
        "job_url": "https://example.com/jobs/1",
        "notes": "Test application",
    }


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_get_application():
    created = client.post("/applications", json=sample_payload())
    assert created.status_code == 201

    application_id = created.json()["id"]
    fetched = client.get(f"/applications/{application_id}")

    assert fetched.status_code == 200
    assert fetched.json()["company"] == "Example Labs"


def test_list_filter_and_stats():
    client.post("/applications", json=sample_payload())

    payload = sample_payload()
    payload["status"] = "Interview"
    client.post("/applications", json=payload)

    assert len(client.get("/applications").json()) == 2
    assert len(client.get("/applications?status=Interview").json()) == 1
    assert client.get("/stats").json()["total"] == 2


def test_update_application():
    created = client.post("/applications", json=sample_payload())
    application_id = created.json()["id"]

    updated = client.patch(
        f"/applications/{application_id}",
        json={"status": "Interview"},
    )

    assert updated.status_code == 200
    assert updated.json()["status"] == "Interview"


def test_delete_application_and_not_found():
    created = client.post("/applications", json=sample_payload())
    application_id = created.json()["id"]

    deleted = client.delete(f"/applications/{application_id}")

    assert deleted.status_code == 204
    assert client.get(f"/applications/{application_id}").status_code == 404