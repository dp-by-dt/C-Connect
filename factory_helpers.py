# File for registering blueprints, extensions, error handlers etc. These would get initialized in app.py

from flask import render_template
from extensions import db, login_manager, csrf, migrate
import pytz
from datetime import datetime, timezone
import logging
from logging.handlers import RotatingFileHandler
import os





#function to register extensions
def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    # Add other extensions here as needed


#function to register blueprints
def register_blueprints(app):
    from blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from blueprints.connections import connections as connections_bp
    app.register_blueprint(connections_bp)

    from blueprints.notifications import notifications
    app.register_blueprint(notifications)


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


# convert utc to ist
def to_ist(utc_dt):
    ist = pytz.timezone('Asia/Kolkata')
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(ist)



#logs errors in the logs/cconnect.log file
def configure_logging(app):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "cconnect.log"),
        maxBytes=1024 * 1024,  # 1 MB per file
        backupCount=5          # keep last 5 logs
    )

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)



# Auto delete old notifications
def register_daily_cleanup(app):
    # initialize attribute if not present
    if not hasattr(app, "_last_notification_cleanup"):
        app._last_notification_cleanup = None

    @app.before_request
    def daily_cleanup():
        now = datetime.now(timezone.utc)
        last = getattr(app, "_last_notification_cleanup", None)

        # run only once/day
        if last is None or (now - last).days >= 1:
            from blueprints.notifications.service import cleanup_old_notifications
            deleted = cleanup_old_notifications()
            app.logger.info(f"Cleaned up {deleted} old notifications.")
            app._last_notification_cleanup = now
