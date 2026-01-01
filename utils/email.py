from flask_mail import Message
from app import mail

def send_reset_email(to_email, reset_url):
    msg = Message(
        subject="Reset your C-Connect password",
        recipients=[to_email]
    )
    msg.body = f"""
Hi,

You requested a password reset.

Click the link below to reset your password:
{reset_url}

This link will expire in 15 minutes.

If you did not request this, you can safely ignore this email.
"""
    mail.send(msg)
