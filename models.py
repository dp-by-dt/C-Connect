from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


#Initialising SQLAlchemy (db) with app
db = SQLAlchemy()


# Creating the db structure
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier
    username = db.Column(db.String(100), nullable=False)  # Name of the user
    email = db.Column(db.String(120), nullable=False, unique=True)  # Email of the user
    password = db.Column(db.String(200), nullable=False)  # Passwords not hashed

    #hashing passwords for security
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    pass