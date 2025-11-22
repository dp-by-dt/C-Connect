from extensions import db
from models import User, Profile
import logging

logger = logging.getLogger(__name__)

def add_user(user_name, email, password):
    """
    Create a new user and an (empty) profile row atomically.
    Returns: True if created, False if email exists.
    Raises: Exception for unexpected DB errors (will rollback).
    """
    # normalize
    email = (email or "").strip().lower()
    username = (user_name or "").strip()

    if User.query.filter_by(email=email).first():
        return False  # user already exists

    try:
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        # Create profile linked to the user (SQLAlchemy will set user_id on flush/commit)
        new_profile = Profile(user=new_user)

        db.session.add(new_user)
        db.session.add(new_profile)

        db.session.commit()
        return True
    except Exception as exc:
        db.session.rollback()
        logger.exception("Error creating user %s: %s", email, exc)
        raise

