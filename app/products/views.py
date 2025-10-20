from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/')
def products_index():
    return "<h3>Products root — тут буде список продуктів (порожньо)</h3>"
