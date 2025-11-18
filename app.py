from flask import Flask, url_for, render_template, request, redirect, make_response
import os
from flask_login import current_user

from setup_db import add_user as adduser_glob

from extensions import login_manager, db



#Creating App instant and Registering Blueprints
def create_app():
    app = Flask(__name__)

    
    #configure the Database
    app.config.from_object('config.Config')

    #initializing the extensions with app
    db.init_app(app)
    #registering loginManager for flask-login
    login_manager.init_app(app)
    #migrate.init_app(app,db) #optional for db migrations
    #csrf.init_app(app) #but later


    #loading user
    @login_manager.user_loader
    def load_user(user_id):
        from models import User  # Importing User model for querying  (import here to avoid circular imports)
        return User.query.get(int(user_id))
    

    
    #create the database if not created(by creating the instance_path folder)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #---------- Register the BluePrints-----------
    # Import and register blueprints
    from blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #add register error handlers (404/500) for later


    #not storing unwanted cache for sensitive pages
    @app.after_request
    def add_header(response):

        #maintains no-cache only for auth blueprint pages when user is logged in
        if current_user.is_authenticated and request.blueprint == 'auth':
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'
        return response

    return app


#-------------------main start ----------
if __name__ == '__main__':
    app = create_app()
    # Create tables once before the first request, optionally here
    with app.app_context(): #won't replace it on each run
        db.create_all() #could also use this in flask CLI

    app.run(debug=True)


