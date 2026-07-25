from app.models import User


def test_register(client):
    response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    assert response.status_code == 201

    user = User.query.filter_by(email="john@example.com").first()
    assert user is not None
def test_register_duplicate_email(client):
    # First registration
    client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    # Attempt to register the same email again
    response = client.post(
        "/api/auth/register",
        json={
            "fullName": "Jane Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "An account with this email already exists."
    assert data["field"] == "email"

    assert User.query.filter_by(email="john@example.com").count() == 1
def test_register_invalid_email(client):
    response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "not-an-email",
            "password": "Password123!"
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["field"] == "email"
def test_register_password_too_short(client):
    response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Pass1"
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Password must be at least 8 characters long."
    assert data["field"] == "password"
def test_register_password_requires_letter_and_number(client):
    response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password"
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Password must include at least one letter and one number."
    assert data["field"] == "password"
def test_register_missing_required_fields(client):
    response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "password": "Password123!"
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Missing required field(s): email."
def test_login_success(client):
    # Register a user
    client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    # Log in
    response = client.post(
        "/api/auth/login",
        json={
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "accessToken" in data
    assert "refreshToken" in data
    assert "user" in data
    assert "account" in data

    assert data["user"]["email"] == "john@example.com"

def test_login_success(client):
    # Register a user
    client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    # Log in
    response = client.post(
        "/api/auth/login",
        json={
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "accessToken" in data
    assert "refreshToken" in data
    assert "user" in data
    assert "account" in data

    assert data["user"]["email"] == "john@example.com"
def test_login_wrong_password(client):
    # Register a user
    client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    # Attempt login with the wrong password
    response = client.post(
        "/api/auth/login",
        json={
            "email": "john@example.com",
            "password": "WrongPassword123!"
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid email or password."
    assert data["field"] == "form"
    
def test_login_nonexistent_email(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "Password123!"
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid email or password."
    assert data["field"] == "form"