from flask import Blueprint

post_bp = Blueprint(
    'post_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from app.posts import views