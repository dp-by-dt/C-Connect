from flask import Blueprint

messages = Blueprint(
                "messages", 
                __name__,
                template_folder='templates',
                static_folder='static',
                static_url_path='/messages/static',
                url_prefix="/messages",
                )

from . import routes
