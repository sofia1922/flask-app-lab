from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from app.forms import LoginForm

users_bp = Blueprint('users', __name__, template_folder='templates')

VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"

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

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['user'] = username
            flash(f"Вітаю, {username}! Вхід успішний ✅", "success")
            return redirect(url_for('users.profile'))
        else:
            flash("Невірне ім’я користувача або пароль!", "danger")
            return redirect(url_for('users.login'))

    if request.method == 'POST' and not form.validate():
        flash("Будь ласка, перевірте правильність введених даних!", "warning")

    return render_template('users/login.html', form=form, title='Вхід')


@users_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        flash("Спочатку увійдіть у систему", "warning")
        return redirect(url_for('users.login'))

    username = session['user']
    cookies = request.cookies
    response = make_response(render_template('users/profile.html', username=username, cookies=cookies, title='Профіль'))

    if request.method == 'POST':
        if 'add_cookie' in request.form:
            key = request.form.get('key')
            value = request.form.get('value')
            expires = request.form.get('expires', type=int)
            if expires:
                response.set_cookie(key, value, max_age=expires)
                flash(f"Кукі '{key}' додано на {expires} сек.", "success")
            else:
                response.set_cookie(key, value)
                flash(f"Кукі '{key}' додано без терміну дії.", "success")

        elif 'delete_cookie' in request.form:
            key = request.form.get('key')
            response.delete_cookie(key)
            flash(f"Кукі '{key}' видалено!", "danger")

        elif 'delete_all' in request.form:
            for key in cookies.keys():
                response.delete_cookie(key)
            flash("Усі кукі видалено!", "danger")

        return response

    return response


@users_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash("Ви вийшли із системи", "info")
    return redirect(url_for('users.login'))

@users_bp.route('/set_theme/<theme>')
def set_theme(theme):
    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('theme', theme)
    flash(f"Тема змінена на {theme} 🎨", "info")
    return response

