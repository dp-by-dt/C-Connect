from models import User, db 


#CRUD helper functions
def add_user(user_name, email, password):
    new_user = User(username=user_name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()