def test_deposit_success(client):
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

    # Deposit money
    response = client.post(
        "/api/transactions/deposit",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 1000
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "account" in data
    assert "transaction" in data

    assert data["transaction"]["type"] == "deposit"
    assert data["transaction"]["amount"] == "1000"
    assert data["transaction"]["balanceAfter"] == "1000"

    assert data["account"]["balance"] == "1000"
    assert data["account"]["currency"] == "NGN"

def test_withdraw_success(client):
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

    # Deposit money first
    client.post(
        "/api/transactions/deposit",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 1000
        },
    )

    # Withdraw part of the money
    response = client.post(
        "/api/transactions/withdraw",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 400
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "account" in data
    assert "transaction" in data

    assert data["transaction"]["type"] == "withdrawal"
    assert data["transaction"]["amount"] == "400"
    assert data["transaction"]["balanceAfter"] == "600"

    assert data["account"]["balance"] == "600"

def test_withdraw_insufficient_funds(client):
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

    # Attempt to withdraw without depositing first
    response = client.post(
        "/api/transactions/withdraw",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 100
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["field"] == "amount"
    assert data["error"] == "Insufficient funds."

def test_transfer_success(client):
    # Register sender
    sender_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    sender_data = sender_response.get_json()
    sender_token = sender_data["accessToken"]

    # Register receiver
    receiver_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "Jane Doe",
            "email": "jane@example.com",
            "password": "Password123!"
        },
    )

    receiver_data = receiver_response.get_json()
    receiver_account_number = receiver_data["account"]["accountNumber"]
    receiver_token = receiver_data["accessToken"]

    # Deposit money into the sender's account
    deposit_response = client.post(
        "/api/transactions/deposit",
        headers={
            "Authorization": f"Bearer {sender_token}"
        },
        json={
            "amount": 1000
        },
    )

    assert deposit_response.status_code == 200

    # Transfer money to the receiver
    response = client.post(
        "/api/transactions/transfer",
        headers={
            "Authorization": f"Bearer {sender_token}"
        },
        json={
            "receiverAccountNumber": receiver_account_number,
            "amount": 400
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "account" in data
    assert "transaction" in data

    assert data["transaction"]["type"] == "transfer_out"
    assert data["transaction"]["amount"] == "400"
    assert data["transaction"]["balanceAfter"] == "600"

    assert data["account"]["balance"] == "600"

    # Check the receiver's account
    receiver_account_response = client.get(
        "/api/accounts/me",
        headers={
            "Authorization": f"Bearer {receiver_token}"
        },
    )

    assert receiver_account_response.status_code == 200

    receiver_account = receiver_account_response.get_json()

    assert receiver_account["account"]["balance"] == "400"

def test_transfer_to_self(client):
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    register_data = register_response.get_json()
    access_token = register_data["accessToken"]
    account_number = register_data["account"]["accountNumber"]

    # Deposit money first
    deposit_response = client.post(
        "/api/transactions/deposit",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 1000
        },
    )

    assert deposit_response.status_code == 200

    # Attempt to transfer to the same account
    response = client.post(
        "/api/transactions/transfer",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "receiverAccountNumber": account_number,
            "amount": 400
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["field"] == "receiverAccountNumber"
    assert data["error"] == "You cannot transfer to your own account."

def test_transfer_receiver_not_found(client):
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    register_data = register_response.get_json()
    access_token = register_data["accessToken"]

    # Deposit money first
    deposit_response = client.post(
        "/api/transactions/deposit",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 1000
        },
    )

    assert deposit_response.status_code == 200

    # Attempt to transfer to a non-existent account
    response = client.post(
        "/api/transactions/transfer",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "receiverAccountNumber": "9999999999",
            "amount": 400
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["field"] == "receiverAccountNumber"
    assert data["error"] == "Receiver account not found."

def test_transfer_insufficient_funds(client):
    # Register sender
    sender_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    sender_data = sender_response.get_json()
    sender_token = sender_data["accessToken"]

    # Register receiver
    receiver_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "Jane Doe",
            "email": "jane@example.com",
            "password": "Password123!"
        },
    )

    receiver_data = receiver_response.get_json()
    receiver_account_number = receiver_data["account"]["accountNumber"]

    # Attempt to transfer without depositing any money
    response = client.post(
        "/api/transactions/transfer",
        headers={
            "Authorization": f"Bearer {sender_token}"
        },
        json={
            "receiverAccountNumber": receiver_account_number,
            "amount": 500
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["field"] == "amount"
    assert data["error"] == "Insufficient funds."

def test_transaction_history(client):
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    register_data = register_response.get_json()
    access_token = register_data["accessToken"]

    # Make a deposit
    client.post(
        "/api/transactions/deposit",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 1000
        },
    )

    # Make a withdrawal
    client.post(
        "/api/transactions/withdraw",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 300
        },
    )

    # Get transaction history
    response = client.get(
        "/api/transactions/history",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "transactions" in data
    assert "page" in data
    assert "perPage" in data
    assert "total" in data

    assert data["total"] == 2
    assert len(data["transactions"]) == 2

def test_airtime_success(client):
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    register_data = register_response.get_json()
    access_token = register_data["accessToken"]

    # Deposit money first
    deposit_response = client.post(
        "/api/transactions/deposit",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 1000
        },
    )

    assert deposit_response.status_code == 200

    # Purchase airtime
    response = client.post(
        "/api/transactions/airtime",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 300,
            "phone": "08012345678"
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "account" in data
    assert "transaction" in data

    assert data["transaction"]["type"] == "airtime"
    assert data["transaction"]["amount"] == "300"
    assert data["transaction"]["balanceAfter"] == "700"
    assert data["transaction"]["counterpartyAccountNumber"] == "08012345678"

    assert data["account"]["balance"] == "700"

def test_airtime_insufficient_funds(client):
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    register_data = register_response.get_json()
    access_token = register_data["accessToken"]

    # Try to buy airtime without depositing money
    response = client.post(
        "/api/transactions/airtime",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 300,
            "phone": "08012345678"
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["field"] == "amount"
    assert data["error"] == "Insufficient funds."

def test_airtime_invalid_phone(client):
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    register_data = register_response.get_json()
    access_token = register_data["accessToken"]

    # Deposit money
    client.post(
        "/api/transactions/deposit",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 1000
        },
    )

    # Try an invalid phone number
    response = client.post(
        "/api/transactions/airtime",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "amount": 300,
            "phone": "123"
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["field"] == "phone"

def test_airtime_missing_required_fields(client):
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        json={
            "fullName": "John Doe",
            "email": "john@example.com",
            "password": "Password123!"
        },
    )

    register_data = register_response.get_json()
    access_token = register_data["accessToken"]

    response = client.post(
        "/api/transactions/airtime",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Missing required field(s): amount, phone."
