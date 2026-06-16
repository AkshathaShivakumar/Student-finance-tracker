from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets


def hash_password(password):
    """Hash a password using Werkzeug."""
    return generate_password_hash(password, method="pbkdf2:sha256")


def verify_password(password, password_hash):
    """Verify a password against its hash."""
    return check_password_hash(password_hash, password)


def generate_verification_token(email):
    """Generate a secure token for email verification."""
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="email-verification-salt")


def verify_verification_token(token, expiration=3600):
    """Verify a verification token and return the email if valid."""
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt="email-verification-salt", max_age=expiration)
        return email
    except Exception:
        return None


def generate_password_reset_token(email):
    """Generate a secure token for password reset."""
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="password-reset-salt")


def verify_password_reset_token(token, expiration=1800):
    """Verify a password reset token and return the email if valid."""
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=expiration)
        return email
    except Exception:
        return None
