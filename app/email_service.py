from flask import current_app
from flask_mail import Mail, Message

mail = Mail()


def send_password_reset_email(email, token):
    """Send a password reset email."""
    reset_url = f"http://localhost:5000/auth/reset-password/{token}"
    subject = "Password Reset Request - Student Finance Tracker"
    body = f"""To reset your password, visit the following link:
{reset_url}

If you did not make this request, please ignore this email.
The link will expire in 30 minutes.
"""
    msg = Message(subject, recipients=[email], body=body)
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_welcome_email(email, username):
    """Send a welcome email to new users."""
    subject = "Welcome to Student Finance Tracker"
    body = f"""Hi {username},

Welcome to Student Finance Tracker! Your account has been successfully created.

Start managing your finances today and reach your savings goals.

Best regards,
Student Finance Tracker Team
"""
    msg = Message(subject, recipients=[email], body=body)
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending welcome email: {e}")
        return False
