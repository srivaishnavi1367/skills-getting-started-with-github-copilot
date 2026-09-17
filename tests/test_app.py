from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_delete_participant_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_delete_missing_participant_returns_404():
    activity_name = "Chess Club"
    email = "missingstudent@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 404
