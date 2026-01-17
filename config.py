import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#admin control panel
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", 314159))  #default admin id if not set in env


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY",'dev-secret')  #later replace with os.urandom(24) if need
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    #for forget password
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    RESET_TOKEN_EXP_MINUTES = 15

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = "no-reply@c-connect.com"


    # Uploads
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER",
        os.path.join(BASE_DIR, "static", "uploads")
    )
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 2 * 1024 * 1024)) #2MB


    SESSION_COOKIE_SECURE = False  # Ensures cookies are sent over HTTPS only... keep False for local dev, set True for production
    SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access to session cookie
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)  # Session lifetime
    REMEMBER_COOKIE_DURATION = timedelta(days=30)  # Duration for "Remember Me" cookie
    
    #setting multiple config classes for different environments
    DEBUG = True  #DevelopmentConfig.. Set to False in production
    TESTING = True
    #production config (debug flase, session cookie secure true, etc) can be added later
    # Notifications expiry hours
    NOTIFICATION_EXPIRY_HOURS = int(os.environ.get("NOTIFICATION_EXPIRY_HOURS", 24))

    

#now adding developmentConfig, productionconfig, testingconfig

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # In development, can be False

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # In production, should be True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for testing
    SESSION_COOKIE_SECURE = False  # In testing, can be False


