from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def get_serializer():
    return URLSafeTimedSerializer(
        current_app.config['SECRET_KEY'],
        salt=current_app.config['SECURITY_PASSWORD_SALT']
    )

def generate_reset_token(email):
    s = get_serializer()
    return s.dumps(email)

def verify_reset_token(token, max_age):
    s = get_serializer()
    return s.loads(token, max_age=max_age)
