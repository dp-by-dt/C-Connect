from extensions import db 
from models import User


#CRUD helper functions
def add_user(user_name, email, password):
    if User.query.filter_by(email=email).first():
        return False  # User already exists
    new_user = User(username=user_name, email=email)
    new_user.set_password(password) #hashing password
    db.session.add(new_user)
    db.session.commit()
    return True
