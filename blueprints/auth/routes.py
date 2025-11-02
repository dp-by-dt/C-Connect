from . import auth
from flask import render_template,  request, flash, redirect, url_for, session, current_app
from setup_db import add_user as adduser_glob
import sqlite3
import os





#Adding users
@auth.route('/add_user',methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Call your add_user function from setup_db
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
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        #check for empty inputs
        if not username or not password:
            flash("Please enter both username and password", "error")
            return redirect(url_for('auth.login'))


        #path of the db file dynamically
        db_path = os.path.join(current_app.instance_path, 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # allows access like a dictionary
        cursor = conn.cursor()

        #sql query on db
        cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
        user = cursor.fetchone() #fetch only one matching
        conn.close()

        # Check if user exists
        if not user:
            flash("Username doesn't exist", "error")
            session.pop('username', None)
            session.pop('loggedin', None)
            session.pop('id', None)

            return redirect(url_for('auth.login'))
        
        elif user['password'] == password: #successful login
            session['username'] = username
            session['loggedin'] = True
            session['id'] = user['id']
            flash("Login successful!", "success")
            return redirect(url_for('auth.dashboard',username=username))
        
        else:
            session.pop('username', None)
            session.pop('loggedin', None)
            session.pop('id', None)

            flash("Invalid Username/Password", "error")
            return redirect(url_for('auth.login'))
        
    return render_template('/auth/login.html')



@auth.route('/dashboard',methods=['GET','POST'])
def dashboard():
    username = session.get('username')
    login_state = session.get('loggedin', False) #avoid crash if key missing

    if not login_state: #not logged in
        flash("Please log in first", "error")
        return redirect(url_for('auth.login'))
    return render_template('/auth/dashboard.html', username=username)


@auth.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))

