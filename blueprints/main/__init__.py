from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates')

from . import routes #general routes
from . import search #search routes