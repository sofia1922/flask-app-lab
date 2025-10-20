from flask import Blueprint, render_template, request, redirect, url_for

users_bp = Blueprint('users', __name__, template_folder='templates')

@users_bp.route('/hi/<string:name>')
def greetings(name):
    name_upper = name.upper()
    age = request.args.get('age', None, type=int)
    return render_template('users/hi.html', name=name_upper, age=age)

@users_bp.route('/admin')
def admin():
    to_url = url_for('users.greetings', name='administrator', age=45)
    print("Redirecting to:", to_url)
    return redirect(to_url)
