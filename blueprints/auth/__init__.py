from flask import Blueprint
from extensions import login_manager
from flask_login import current_user
from flask import request

auth = Blueprint(
            'auth', 
            __name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='/auth/static'
        )



from . import routes # Import routes to register them with the blueprint



#loading user
@login_manager.user_loader
def load_user(user_id):
    from models import User  # Importing User model for querying  (import here to avoid circular imports)
    return User.query.get(int(user_id))


#not storing unwanted cache for sensitive pages
@auth.after_app_request
def add_header(response):

    #maintains no-cache only for auth blueprint pages when user is logged in
    if current_user.is_authenticated and request.blueprint == 'auth':
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
    return response