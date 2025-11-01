from flask_sqlalchemy import SQLAlchemy


#Initialising SQLAlchemy (db) with app
db = SQLAlchemy()


# Creating the db structure
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier
    username = db.Column(db.String(100), nullable=False)  # Name of the user
    email = db.Column(db.String(120), nullable=False, unique=True)  # Email of the user
    password = db.Column(db.String(200), nullable=False)  # Hashed password
