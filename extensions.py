#----Initialise the things here that will be used across the application----

from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_migrate import Migrate

# Initializing SQLAlchemy
db = SQLAlchemy()

# Initializing Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirect to 'auth.login' for @login_required
login_manager.login_message_category = 'info'  # Flash category for login messages

# # Initializing Migrate (optional, for database migrations)
# migrate = Migrate()

# You can add more extensions as needed like csrf protection, mail, etc.

