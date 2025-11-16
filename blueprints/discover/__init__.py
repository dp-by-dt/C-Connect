from flask import Blueprint

discover = Blueprint('discover', __name__, template_folder='templates')

from . import routes
