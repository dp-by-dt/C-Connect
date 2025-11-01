from . import auth
from flask import render_template,  request
from setup_db import add_user as adduser_glob

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
            return "Email already exists"


        # After adding user, redirect to home or another page
        return render_template('auth/signup_success.html', username=username)
        #return redirect(url_for('show_users'))

    # If GET request, just render the base template with form
    return render_template('/auth/signup.html')

@auth.route('/signup_success')
def signup_success():
    return render_template('/auth/signup_success.html')
