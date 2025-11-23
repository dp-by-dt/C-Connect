from flask import Blueprint

connections = Blueprint('connections', __name__, template_folder='templates')

from . import routes  # noqa
