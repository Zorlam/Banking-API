def test_get_my_account(client):
    # Register a new user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    # Get the access token from the registration response
    access_token = register_response.get_json()["accessToken"]

    # Request the account information
    response = client.get(
        "/api/accounts/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "account" in data
    assert "accountNumber" in data["account"]
    assert "balance" in data["account"]
    assert data["account"]["currency"] == "NGN"


def test_get_my_account_without_token(client):
    response = client.get("/api/accounts/me")

    assert response.status_code == 401

    data = response.get_json()

    assert data["msg"] == "Missing Authorization Header"


def test_get_my_account_invalid_token(client):
    response = client.get(
        "/api/accounts/me",
        headers={
            "Authorization": "Bearer fake-invalid-token"
        },
    )

    assert response.status_code == 422

    data = response.get_json()

    assert data["msg"] == "Not enough segments"


def test_change_password_success(client):
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    # Get the access token
    access_token = register_response.get_json()["accessToken"]

    # Change password
    response = client.post(
        "/api/accounts/change-password",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "currentPassword": "Password123!",
            "newPassword": "NewPassword123!"
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Password changed successfully."

    # Verify the password actually changed
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "john@example.com",
            "password": "NewPassword123!"
        },
    )

    assert login_response.status_code == 200

    login_data = login_response.get_json()

    assert "accessToken" in login_data

def test_change_password_wrong_current_password(client):
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    # Get the access token
    access_token = register_response.get_json()["accessToken"]

    # Try to change the password using the wrong current password
    response = client.post(
        "/api/accounts/change-password",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "currentPassword": "WrongPassword123!",
            "newPassword": "NewPassword123!"
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["field"] == "currentPassword"
    assert data["error"] == "Current password is incorrect."

def test_change_password_same_as_current(client):
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    # Get the access token
    access_token = register_response.get_json()["accessToken"]

    # Try to change to the same password
    response = client.post(
        "/api/accounts/change-password",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "currentPassword": "Password123!",
            "newPassword": "Password123!"
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["field"] == "newPassword"
    assert (
        data["error"]
        == "New password must be different from the current password."
    )

def test_change_password_weak_new_password(client):
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    # Get the access token
    access_token = register_response.get_json()["accessToken"]

    # Try to change to a weak password
    response = client.post(
        "/api/accounts/change-password",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "currentPassword": "Password123!",
            "newPassword": "1234567"
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["field"] == "password"
    assert data["error"] == "Password must be at least 8 characters long."

def test_change_password_missing_required_fields(client):
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    # Get the access token
    access_token = register_response.get_json()["accessToken"]

    # Send an empty request body
    response = client.post(
        "/api/accounts/change-password",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert (
        data["error"]
        == "Missing required field(s): currentPassword, newPassword."
    )