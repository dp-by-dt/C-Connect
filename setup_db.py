from extensions import db 
from models import User


#CRUD helper functions
def add_user(user_name, email, password):
    '''return False if user exists, else add the user and returns true'''
    user_to_db = User.query.filter_by(email=email).first()
    if user_to_db:
        return False  # User already exists
    new_user = User(username=user_name, email=email)
    new_user.set_password(password) #hashing password
    db.session.add(new_user)
    db.session.commit()
    return True
