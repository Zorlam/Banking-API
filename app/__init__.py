import os
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman
from dotenv import load_dotenv

from app.extensions import db, jwt, limiter

load_dotenv()


def _normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


def create_app(testing=False, test_config=None):
    app = Flask(__name__)
    app.config["TESTING"] = testing

    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] = _normalize_database_url(
        os.environ.get("DATABASE_URL", "sqlite:///zenith.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
    app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 30))
    )
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
        days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 7))
    )
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    is_production = os.environ.get("FLASK_ENV") == "production"
    Talisman(
        app,
        force_https=is_production,
        strict_transport_security=is_production,
        strict_transport_security_max_age=31536000,
        content_security_policy={
            "default-src": "'none'",
        },
        content_security_policy_nonce_in=None,
        referrer_policy="no-referrer",
        frame_options="DENY",
        x_content_type_options=True,
        x_xss_protection=False,
    )

    frontend_origin = os.environ.get("FRONTEND_ORIGIN", "http://localhost:3000")
    CORS(app, resources={r"/api/*": {"origins": frontend_origin}}, supports_credentials=True)

    from app.routes.auth import auth_bp
    from app.routes.accounts import accounts_bp
    from app.routes.transactions import transactions_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(accounts_bp, url_prefix="/api/accounts")
    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")

    from app.errors import register_error_handlers
    register_error_handlers(app)

    _db_initialized = {"done": False}

    @app.before_request
    def _init_db_once():
        if not _db_initialized["done"]:
            _db_initialized["done"] = True
            db.create_all()

            if not app.config["TESTING"]:
                from app.seed import seed_demo_data
                seed_demo_data()

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app 