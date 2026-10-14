import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_root_redirect():
    # Arrange & Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities():
    # Arrange & Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_for_activity_success():
    # Arrange
    activity_name = "Debate Team"
    test_email = "newstudent@mergington.edu"

    # Ensure clean state
    if test_email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(test_email)

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {test_email} for {activity_name}"}
    assert test_email in activities[activity_name]["participants"]


def test_signup_duplicate_fails():
    # Arrange
    activity_name = "Chess Club"
    existing_student = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_student}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_signup_nonexistent_activity():
    # Arrange
    invalid_activity = "NonExistentClub"
    test_email = "anyone@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{invalid_activity}/signup",
        params={"email": test_email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
