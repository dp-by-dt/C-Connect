from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db


# Creating the db structure
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier
    username = db.Column(db.String(100), nullable=False)  # Name of the user (later can add this unique if needed)
    email = db.Column(db.String(120), nullable=False, unique=True)  # Email of the user
    password = db.Column(db.String(200), nullable=False)  # Passwords not hashed yet (done in setup_db.py)

    #hashing passwords for security
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    pass



# PROFILE table
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,unique=True)  # Foreign key to User

    bio = db.Column(db.String(500), nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)  # URL to profile
    department = db.Column(db.String(100), nullable=True)
    year=db.Column(db.String(20),nullable=True)
    interests=db.Column(db.String(300),nullable=True) #optional now

    user = db.relationship('User', backref=db.backref('profiles', lazy=True, uselist=False))


# CONNECTIONS
class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who initiated the connection
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who is targetted to connect

    status = db.Column(db.String(20), nullable=False) #pending, accepted, blocked
    created_at = db.Column(db.DateTime, default=db.func.now()) #current_timestamp())

    user = db.relationship('User', foreign_keys=[user_id], backref='sent_requests')
    connected_user = db.relationship('User', foreign_keys=[target_user_id], backref='received_requests')


#optional visibility table
''' Later we add option for privacy options like, what option can be viewed by who (like the owner-private, or for all- public)'''

