from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/')
def list_products():
    items = [
        {"name": "Вітаміни C", "price": 120},
        {"name": "Парацетамол", "price": 80},
        {"name": "Назол", "price": 150},
    ]
    return render_template('products/list.html', items=items, title='Список товарів')
