from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_signup_for_activity_success():
    activity_name = "Chess Club"
    email = "newstudent-success@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]

    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)


def test_duplicate_signup_is_rejected():
    activity_name = "Programming Class"
    email = "duplicate-check@mergington.edu"

    activities[activity_name]["participants"].append(email)

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"

    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)


def test_delete_participant_from_activity():
    activity_name = "Chess Club"
    email = "newstudent-delete@mergington.edu"

    activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_delete_missing_participant_returns_404():
    activity_name = "Chess Club"
    email = "missingstudent@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
