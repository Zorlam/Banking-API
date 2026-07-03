# Zenith — Backend

A production-deployed Flask REST API powering a banking-style fintech application. The backend provides authentication, account management, transaction processing, and secure money transfers using PostgreSQL in production and SQLite for local development.

## Live Deployment

* **Backend API:** https://banking-backend-2mwq.onrender.com
* **Frontend:** https://keen-pavlova-f4dc6e.netlify.app
* **Database:** Neon PostgreSQL (production)
* Frontend Repository: https://github.com/Zorlam/banking-frontend

## Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* PostgreSQL (Neon)
* SQLite (local development)
* Flask-JWT-Extended
* Flask-CORS
* Flask-Talisman
* Gunicorn
* bcrypt

## Setup

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

# Fill in the required environment variables

python run.py
```

The development server runs on:

```
http://127.0.0.1:5050
```

For production, the application is served using Gunicorn.

## Environment Variables

Required variables:

```
SECRET_KEY=
JWT_SECRET_KEY=
DATABASE_URL=
JWT_ACCESS_TOKEN_EXPIRES_MINUTES=
JWT_REFRESH_TOKEN_EXPIRES_DAYS=
FRONTEND_ORIGIN=
```

See `.env.example` for the complete template.

## API

All endpoints are available under `/api`.

| Method | Endpoint                    | Authentication | Description                        |
| ------ | --------------------------- | -------------- | ---------------------------------- |
| POST   | `/auth/register`            | No             | Register a new user                |
| POST   | `/auth/login`               | No             | Authenticate user                  |
| POST   | `/auth/refresh`             | Refresh Token  | Generate a new access token        |
| GET    | `/auth/me`                  | Access Token   | Get authenticated user             |
| GET    | `/accounts/me`              | Access Token   | Retrieve account balance           |
| POST   | `/accounts/change-password` | Access Token   | Change account password            |
| GET    | `/transactions/history`     | Access Token   | View paginated transaction history |
| POST   | `/transactions/deposit`     | Access Token   | Deposit funds                      |
| POST   | `/transactions/withdraw`    | Access Token   | Withdraw funds                     |
| POST   | `/transactions/transfer`    | Access Token   | Transfer funds between accounts    |
| POST   | `/transactions/airtime`     | Access Token   | Purchase airtime                   |

All responses are JSON.

## Features

* JWT authentication with access and refresh tokens
* Secure password hashing using bcrypt
* PostgreSQL support for production deployments
* SQLite support for local development
* Atomic money transfers using database transactions
* Server-side validation for user input
* Transaction ledger with running account balances
* Money stored as integer minor units (kobo) to prevent floating-point precision errors
* Automatic database initialization
* CORS configuration for a separate frontend application
* Rate limiting on authentication endpoints
* Security headers using Flask-Talisman
* HTTPS enforcement in production
* Request size limits to reduce abuse

## Security

Current security measures include:

* bcrypt password hashing
* JWT-based authentication
* Rate limiting on login, registration, refresh, and password change endpoints
* HTTPS enforcement in production
* Security headers (Content Security Policy, X-Frame-Options, Referrer Policy, X-Content-Type-Options)
* Maximum request size limits
* Environment-based secrets
* Server-side validation for all user input

## Architecture

The project follows Flask's application factory pattern.

```
app/
├── routes/
│   ├── auth.py
│   ├── accounts.py
│   └── transactions.py
├── models.py
├── validation.py
├── errors.py
├── extensions.py
└── __init__.py
```

## Known Limitations

This project is intended as a learning project and portfolio demonstration.

Current limitations include:

* No email verification
* No token revocation or refresh token rotation
* No idempotency keys for transaction requests
* No KYC, fraud detection, or regulatory compliance
* No database migration system (Flask-Migrate/Alembic)

## License

This project is provided for educational and portfolio purposes.
