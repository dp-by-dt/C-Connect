# File for registering blueprints, extensions, error handlers etc. These would get initialized in app.py

from flask import render_template
from extensions import db, login_manager


#function to register extensions
def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    # Add other extensions here as needed


#function to register blueprints
def register_blueprints(app):
    from blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #can add more blueprints here as needed


#function to register error handlers
def register_errorhandlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # In case of a database error
        return render_template('500.html'), 500