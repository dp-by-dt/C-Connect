from . import auth
from flask import render_template, request, flash, redirect, url_for, session, current_app, make_response
from setup_db import add_user as adduser_glob
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


# Adding users (Signup)
@auth.route('/add_user', methods=['GET', 'POST'])
def add_user_route():
    # CHANGE: Redirect logged-in users to dashboard (prevents re-signup)
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')  # hashing done in 'setup_db.py'

        # Call your add_user function from setup_db (hashing is in here)
        success = adduser_glob(username, email, password)
        if not success:
            flash("Email already exists", "error")
            return redirect(url_for('auth.add_user_route'))

        # After adding user, redirect to success page
        return redirect(url_for('auth.signup_success', username=username))

    # If GET request, just render the signup template
    return render_template('/auth/signup.html')


@auth.route('/signup_success')
def signup_success():
    # Get username from URL parameters
    username = request.args.get('username', 'User')
    return render_template('/auth/signup_success.html', username=username)


# Login Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # CHANGE: Redirect logged-in users to dashboard (prevents re-login)
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        # CHANGE: Login with EMAIL instead of username (more reliable and standard)
        email = request.form.get('email')  # Changed from 'username' to 'email'
        password = request.form.get('password')
        
        # Query user by EMAIL instead of username
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)  # Log the user in
            flash('Login successful! Welcome back.', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            # CHANGE: More specific error message
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


# Dashboard Route
@auth.route('/dashboard')
@login_required  # this decorator restricts access to logged-in users only
def dashboard():
    # CHANGE: Pass more user info for future scalability
    # Query a few suggested users (excluding self) for "People You May Know" section
    suggested_users = User.query.filter(User.id != current_user.id).limit(5).all()
    
    return render_template('auth/dashboard.html', 
                         username=current_user.username,
                         email=current_user.email,
                         suggested_users=suggested_users)


# Logout Route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for('main.home'))  # CHANGE: Redirect to home instead of login