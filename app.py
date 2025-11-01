from flask import Flask, url_for, render_template, request, redirect
import os

from models import db  # Just the db object
from setup_db import add_user as adduser_glob
from models import User  # Importing User model for querying



app = Flask(__name__)


#create the database if not created(by creating the instance_path folder)
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

#configure the Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(app.instance_path, 'database.db') #connects sqlite to that .db file in instance folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #avoid unwanted change tracking

db.init_app(app) # Binding db to the flask app 


#-------------- Routes ------------------

#render the base html template
@app.route('/')
def base():
    return render_template('base.html')


#make the buttons work to go to the respective webpages
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact(var_name="Jennifer"):
    return render_template('contact.html',name=var_name)


#Testing the db
@app.route('/show_users')
def show_users():
    users = User.query.all()  # Fetch all users
    arr = [(user.id, user.username, user.email, user.password) for user in users]
    if not arr:
        return 'No users found'
    return '<br>'.join([f'Id {id}, Username: {username}, Email: {email}, Pass: {password}' for id, username, email, password in arr])


#Adding users
@app.route('/add_user',methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Call your add_user function from setup_db
        success = adduser_glob(username, email, password)
        if not success:
            return "Email already exists"


        # After adding user, redirect to home or another page
        return render_template('signup_success.html', username=username)
        #return redirect(url_for('show_users'))

    # If GET request, just render the base template with form
    return render_template('signup.html')



if __name__ == '__main__':
    # Create tables once before the first request, optionally here
    with app.app_context(): #won't replace it on each run
        db.create_all() #could also use this in flask CLI

    app.run(debug=True)