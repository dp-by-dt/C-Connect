from flask import Flask, url_for, render_template, request, redirect, make_response
import os
from flask_login import LoginManager, current_user

from models import db  # Just the db object
from setup_db import add_user as adduser_glob
from models import User  # Importing User model for querying


#registering blueprints
def create_app():
    app = Flask(__name__)

    
    #configure the Database
    app.config.from_object('config.Config')

    #registering loginManager for flask-login
    login_manager = LoginManager()
    login_manager.init_app(app)

    #Flask-Login will redirect unauthorized users to the right login route
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'   # optional


    #loading user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    #not storing unwanted cache for sensitive pages
    @app.after_request
    def add_header(response):

        #maintains no-cache only for auth blueprint pages when user is logged in
        if current_user.is_authenticated and request.blueprint == 'auth':
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'
        return response


    db.init_app(app) # Binding db to the flask app 


    
    #create the database if not created(by creating the instance_path folder)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # Import and register blueprints
    from blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


#-------------------main start ----------
if __name__ == '__main__':
    app = create_app()
    # Create tables once before the first request, optionally here
    with app.app_context(): #won't replace it on each run
        db.create_all() #could also use this in flask CLI

    app.run(debug=True)






#-------------- Routes ------------------

#render the base html template
# @app.route('/')
# def base():
#     return render_template('base.html')


# #make the buttons work to go to the respective webpages
# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/contact')
# def contact(var_name="Jennifer"):
#     return render_template('contact.html',name=var_name)


# #Testing the db
# @app.route('/show_users')
# def show_users():
#     users = User.query.all()  # Fetch all users
#     arr = [(user.id, user.username, user.email, user.password) for user in users]
#     if not arr:
#         return 'No users found'
#     return '<br>'.join([f'Id {id}, Username: {username}, Email: {email}, Pass: {password}' for id, username, email, password in arr])


# #Adding users
# @app.route('/add_user',methods=['GET', 'POST'])
# def add_user_route():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')

#         # Call your add_user function from setup_db
#         success = adduser_glob(username, email, password)
#         if not success:
#             return "Email already exists"


#         # After adding user, redirect to home or another page
#         return render_template('signup_success.html', username=username)
#         #return redirect(url_for('show_users'))

#     # If GET request, just render the base template with form
#     return render_template('signup.html')



