# Zenith — Backend

A production-deployed Flask REST API powering a banking-style fintech application. The backend implements JWT-based authentication, account management, transaction processing, and secure money transfers using PostgreSQL in production. For local development, the project supports both SQLite and Docker Compose with PostgreSQL.

---

## Live Deployment

- **Backend API:** https://banking-backend-2mwq.onrender.com
- **Frontend:** https://keen-pavlova-f4dc6e.netlify.app
- **Production Database:** Neon PostgreSQL
- **Frontend Repository:** https://github.com/Zorlam/banking-frontend

---

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL (Neon)
- SQLite
- Docker
- Docker Compose
- Flask-JWT-Extended
- Flask-CORS
- Flask-Talisman
- Gunicorn
- bcrypt

---

## Features

- **Docker support:** Containerized Flask backend with Docker Compose for local development.
- JWT authentication using access and refresh tokens.
- Secure password hashing with bcrypt.
- PostgreSQL support for production deployments.
- SQLite support for lightweight local development.
- Atomic money transfers using database transactions.
- Server-side validation for all user input.
- Transaction ledger with running balances.
- Money stored as integer minor units (kobo) to eliminate floating-point precision errors.
- Automatic database initialization and demo data seeding.
- CORS configuration for a separate frontend.
- Rate limiting on authentication endpoints.
- Security headers using Flask-Talisman.
- HTTPS enforcement in production.
- Request size limits to reduce abuse.

---

## Running with Docker Compose

Run the backend together with a local PostgreSQL database.

### Prerequisites

- Docker Desktop

### Start the application

```bash
docker compose up --build
```

The API will be available at:

```
http://localhost:5050
```

The first request automatically creates the database tables and seeds the demo data.

### Stop the application

```bash
docker compose down
```

To remove the containers and PostgreSQL data volume:

```bash
docker compose down -v
```

---

## Local Setup (Without Docker)

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

In production, the application is served with Gunicorn.

---

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

---

## API

All endpoints are available under `/api`.

| Method | Endpoint | Authentication | Description |
|--------|----------|---------------|-------------|
| POST | `/auth/register` | No | Register a new user |
| POST | `/auth/login` | No | Authenticate a user |
| POST | `/auth/refresh` | Refresh Token | Generate a new access token |
| GET | `/auth/me` | Access Token | Retrieve authenticated user |
| GET | `/accounts/me` | Access Token | Retrieve account details |
| POST | `/accounts/change-password` | Access Token | Change account password |
| GET | `/transactions/history` | Access Token | Retrieve paginated transaction history |
| POST | `/transactions/deposit` | Access Token | Deposit funds |
| POST | `/transactions/withdraw` | Access Token | Withdraw funds |
| POST | `/transactions/transfer` | Access Token | Transfer funds |
| POST | `/transactions/airtime` | Access Token | Purchase airtime |

All responses are returned as JSON.

---

## Security

Current security measures include:

- bcrypt password hashing
- JWT-based authentication
- Rate limiting on login, registration, refresh, and password change endpoints
- HTTPS enforcement in production
- Security headers (Content Security Policy, X-Frame-Options, Referrer Policy, X-Content-Type-Options)
- Maximum request size limits
- Environment-based secrets
- Comprehensive server-side validation

---

## Architecture

The project follows Flask's application factory pattern, separating routing, models, extensions, validation, and error handling into modular components for maintainability.

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
├── seed.py
└── __init__.py
```

High-level architecture:

```
                 Frontend (Next.js)
                        │
                  HTTP / JSON
                        │
                        ▼
               Flask + Gunicorn API
                        │
                  SQLAlchemy ORM
                        │
                        ▼
                 PostgreSQL Database
```

---

## Known Limitations

This project is intended as a portfolio and learning project.

Current limitations include:

- No email verification
- No refresh token rotation or token revocation
- No idempotency keys for transaction requests
- No KYC or fraud detection
- No regulatory compliance features
- No database migration system (Alembic / Flask-Migrate)

---

## License

This project is provided for educational and portfolio purposes.
