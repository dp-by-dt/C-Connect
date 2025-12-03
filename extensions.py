#----Initialise the things here that will be used across the application----

from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initializing SQLAlchemy
db = SQLAlchemy()

# Initializing Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirect to 'auth.login' for @login_required
login_manager.login_message_category = 'info'  # Flash category for login messages

# # Initializing Migrate (optional, for database migrations)
migrate = Migrate()

# You can add more extensions as needed like csrf protection, mail, etc.


#initiating csrf protection
csrf = CSRFProtect()

#rate limiter
limiter = Limiter(
    key_func=get_remote_address, #rate limit by ip
    default_limits=["100 per hour"], #app wide default
    storage_uri="memory://" #use redis for production: "redis://localhost:6379"
)
