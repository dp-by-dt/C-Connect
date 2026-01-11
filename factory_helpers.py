# File for registering blueprints, extensions, error handlers etc. These would get initialized in app.py

from flask import render_template
from extensions import db, login_manager, csrf, migrate, limiter
import pytz
from datetime import datetime, timezone, timedelta
import time
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_limiter.util import get_remote_address
from flask_login import current_user
from config import ADMIN_USER_ID

from models import ProfileVisit, Message, CampusBoardPost


#Secure headers to stop xss, script injection, image injection etc
def register_security_headers(app):
    """Add secure HTTP headers"""
    @app.after_request
    def set_secure_headers(response):
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "img-src 'self' data: blob: https:; "# Allow external images
            "style-src 'self' 'unsafe-inline' https:; "# ADD https: for CDNs
            "script-src 'self' 'unsafe-inline' https:; "# ADD https: for JS
            "font-src 'self' https: data:; "# Google Fonts
            "connect-src 'self' https:;"  # ← ADD https: for CDNs/maps
        )
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=()'
        return response





#function to register extensions
def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app=app)#rate limiter
    # Add other extensions here as needed



    #----- Later add this shared limiter is needed
    #---- But make sure to replace @limiter.limit("5 per minute") with @app.login_limiter	
    # Shared login brute-force protection (10 attempts/hour per IP)
    # login_limiter = limiter.shared_limit("10 per hour", key_func=get_remote_address)
    
    # # Export for blueprint use
    # app.login_limiter = login_limiter



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

    from blueprints.posts import posts_bp
    app.register_blueprint(posts_bp)

    from blueprints.messages import messages
    app.register_blueprint(messages)

    from blueprints.vibe import vibe_bp
    app.register_blueprint(vibe_bp)

    from blueprints.campus_board import campus_board_bp
    app.register_blueprint(campus_board_bp)



    #can add more blueprints here as needed


#function to register error handlers
def register_errorhandlers(app):

    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # safety for failed transactions
        return render_template('errors/500.html'), 500



# convert utc to ist
def to_ist(utc_dt):
    ist = pytz.timezone('Asia/Kolkata')
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(ist)


#======== Admin control panel ========
def is_admin():
    return (
        current_user.is_authenticated and 
        current_user.id == ADMIN_USER_ID
    )




#logs errors in the logs/cconnect.log file
def configure_logging(app):
    """Configure Flask app logging to prevent config dumps"""
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
    app.logger.setLevel(logging.INFO)  #prevents config dumps



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


# Delete old profile-view rows
def register_profilevisit_cleanup(app):
    last_cleanup = {'t': 0}

    @app.before_request
    def cleanup_visits():
        now = time.time()
        if now - last_cleanup['t'] < 3600:  # run once every hour
            return

        last_cleanup['t'] = now
        cutoff = datetime.now(timezone.utc) - timedelta(days=7) #cleans earlier than 7 days

        try:
            deleted = ProfileVisit.query.filter(ProfileVisit.timestamp < cutoff).delete()
            db.session.commit()
            if deleted:
                app.logger.info(f"ProfileVisit cleanup removed {deleted} rows")
        except Exception as e:
            db.session.rollback()
            app.logger.error("ProfileVisit cleanup failed: %s", str(e))



# delete old messages (one-to-one chat) : default set as 24 hours
def cleanup_expired_messages(): #message cleanup helper function
    Message.query.filter(
        Message.expires_at < datetime.now(timezone.utc),
        Message.is_saved == False
    ).delete()
    db.session.commit()



# delete expired posts from the notice board (campus_board)
def cleanup_expired_posts():
    now = datetime.now(timezone.utc)
    CampusBoardPost.query.filter(
        CampusBoardPost.expires_at < now
    ).delete()
    db.session.commit()
