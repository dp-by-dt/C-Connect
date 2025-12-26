from flask import Blueprint


posts_bp = Blueprint(
            'posts', 
            __name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='/posts/static',
            #url_prefix="/posts" #---seems not to be needed (can be added if it is best practice)
        )

from . import routes # Import routes to register them with the blueprint