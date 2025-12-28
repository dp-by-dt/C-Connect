from flask import Blueprint


vibe_bp = Blueprint(
            'vibe', 
            __name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='/posts/static',
            url_prefix="/vibe" #---seems not to be needed (can be added if it is best practice)
        )

from . import routes # Import routes to register them with the blueprint