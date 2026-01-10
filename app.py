from flask import Flask, url_for, render_template, request, redirect, make_response
import os
from extensions import db
from factory_helpers import register_blueprints, register_errorhandlers, register_extensions, configure_logging, register_security_headers
from factory_helpers import to_ist, register_daily_cleanup, register_profilevisit_cleanup
from flask_login import current_user
from datetime import date
from models import VibeQuestion, VibeResponse, VibeDailyState
from flask import g
from flask_mail import Mail


mail = Mail()

#Creating App instant and Registering Blueprints
def create_app():
    app = Flask(__name__, instance_relative_config=True) #db path inside the instance/ folder always resolves correctly

    #configure the Database
    app.config.from_object('config.Config')

    mail.init_app(app)
    #migrate.init_app(app,db) #optional for db migrations
    #csrf.init_app(app) #but later in factory_helpers file or somewhere

    #------ helper functions -----
    @app.context_processor
    def utility_processor():
        return dict(to_ist=to_ist)
    

    # --------- Before request (for vibe question ) --------
    # to block user to access the app before answering the question 
    @app.before_request
    def enforce_daily_vibe():
        if not current_user.is_authenticated:
            return

        allowed_endpoints = {
            "vibe.daily_vibe",
            "vibe.respond_vibe",
            "auth.logout",
            "static"
        }

        if request.endpoint in allowed_endpoints:
            return

        question = VibeQuestion.query.filter_by(active_date=date.today()).first()
        if not question:
            return

        voted = VibeResponse.query.filter_by(
            question_id=question.id,
            user_id=current_user.id
        ).first()

        if not voted:
            return redirect(url_for("vibe.daily_vibe"))
        

    # color injection for the theme according to the vibe
    @app.before_request
    def inject_vibe_color():
        g.vibe_color = None

        state = VibeDailyState.query.get(date.today())
        if state:
            g.vibe_color = state.accent_color



 
    #create the database if not created(by creating the instance_path folder)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #---------- Register the Extensions and BluePrints-----------
    register_extensions(app)
    register_security_headers(app)
    register_blueprints(app)
    register_errorhandlers(app)
    configure_logging(app)

    #daily cleanup triggering for old notifications
    register_daily_cleanup(app)
    #cleanup old profile_visit
    register_profilevisit_cleanup(app)


    #----------- Debugging the routes urls
    # Add to your app.py (TEMP):
    @app.route('/debug-routes')
    def debug_routes():
        import urllib.parse
        output = []
        for rule in app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)
            
            methods = ','.join(rule.methods)
            url = urllib.parse.unquote("{0}".format(rule))
            line = urllib.parse.unquote("({0}) {1} {2}".format(methods, url, options))
            output.append(line)
        
        return "<br>".join(sorted(output))

        
    return app






#-------------------main start ----------
if __name__ == '__main__':
    app = create_app()
    # Create tables once before the first request, optionally here
    with app.app_context(): #won't replace it on each run
        db.create_all() #could also use this in flask CLI

    app.run(debug=True)


