from flask import Flask, url_for, render_template, request, redirect, make_response
import os
from extensions import db
from factory_helpers import register_blueprints, register_errorhandlers, register_extensions



#Creating App instant and Registering Blueprints
def create_app():
    app = Flask(__name__, instance_relative_config=True) #db path inside the instance/ folder always resolves correctly

    #configure the Database
    app.config.from_object('config.Config')

    #migrate.init_app(app,db) #optional for db migrations
    #csrf.init_app(app) #but later in factory_helpers file or somewhere

 
    #create the database if not created(by creating the instance_path folder)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #---------- Register the Extensions and BluePrints-----------
    register_blueprints(app)
    register_extensions(app)
    register_errorhandlers(app)

    
    return app


#-------------------main start ----------
if __name__ == '__main__':
    app = create_app()
    # Create tables once before the first request, optionally here
    with app.app_context(): #won't replace it on each run
        db.create_all() #could also use this in flask CLI

    app.run(debug=True)


