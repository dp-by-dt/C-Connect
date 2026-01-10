from flask import Blueprint

campus_board_bp = Blueprint(
    "campus_board_bp",
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/posts/static',
    url_prefix="/campus-board"
)

from . import routes

