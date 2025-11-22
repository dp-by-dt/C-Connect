"""Populate the db tables for testing purpose"""

from app import create_app
from models import db, User, Profile
from werkzeug.security import generate_password_hash
import random

app = create_app()
app.app_context().push()


#for seeding `users` table
sample_users = [
    {"username": "arjun", "email": "arjun@uni.com", "password": "arjun"},
    {"username": "maria", "email": "maria@uni.com", "password": "maria"},
    {"username": "rahul", "email": "rahul@uni.com", "password": "rahul"},
    {"username": "sneha", "email": "sneha@uni.com", "password": "sneha"},
    {"username": "kiran", "email": "kiran@uni.com", "password": "kiran"},
    {"username": "rakesh", "email": "rakesh@uni.com", "password": "rakesh@123"},
]


for u in sample_users:
    user = User(
        username=u["username"],
        email=u["email"],
        password=generate_password_hash(u["password"])
    )
    db.session.add(user)
    db.session.flush()
    profile = Profile(
        user_id=user.id,
        bio="Hello, I'm " + u["username"].title(),
        department=random.choice(["ECE","Physics","Chemistry","social", "journalism"]),
        year=random.choice(["1st Year","2nd Year","3rd Year","4th Year"]),
        interests=random.choice(["AI, Robotics","Python,Physics","Maths,Economics","Dance,Music","Literature,Karate"])
    )
    db.session.add(profile)

#committing all the added users and profile all at once
db.session.commit()

print("Seed completed.")
