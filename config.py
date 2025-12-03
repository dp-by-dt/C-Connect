import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# file uploads (local)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB

# Notification auto delete
NOTIFICATION_EXPIRY_HOURS = 24

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY",'dev-secret')  #later replace with os.urandom(24) if need
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = False  # Ensures cookies are sent over HTTPS only... keep False for local dev, set True for production
    SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access to session cookie
    REMEMBER_COOKIE_DURATION = timedelta(days=30)  # Duration for "Remember Me" cookie
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)  # Session lifetime

    #setting multiple config classes for different environments
    DEBUG = True  #DevelopmentConfig.. Set to False in production
    #production config (debug flase, session cookie secure true, etc) can be added later
    

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


