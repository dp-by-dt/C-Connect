from . import auth
from flask import render_template,  request, flash, redirect, url_for, session, current_app
from setup_db import add_user as adduser_glob
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user





#Adding users
@auth.route('/add_user',methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password') #hashing done in 'setup_db.py'

        # Call your add_user function from setup_db (hashing is in here)
        success = adduser_glob(username, email, password)
        if not success:
            flash("Email already exists", "error")
            return redirect(url_for('auth.add_user_route'))

        # After adding user, redirect to home or another page
        return redirect(url_for('auth.signup_success',username=username))
    
        # return render_template('auth/signup_success.html', username=username)

        #return redirect(url_for('show_users'))

    # If GET request, just render the base template with form
    return render_template('/auth/signup.html')

@auth.route('/signup_success')
def signup_success():
    return render_template('/auth/signup_success.html', username=request.args.get('username'))





@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()#use sqlalchemy to get user by username

        if user and check_password_hash(user.password, password):
            login_user(user)  # Log the user in
            flash('Login successful!', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')




@auth.route('/dashboard')
@login_required  # this decorator restricts access to logged-in users only
def dashboard():
    # current_user is the loaded User model object for logged in user
    return render_template('auth/dashboard.html', username=current_user.username)



@auth.route('/logout')
@login_required #same as before
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))

