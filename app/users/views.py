from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.users.models import User
from app.forms import LoginForm, RegisterForm, UpdateAccountForm, ChangePasswordForm
from app.utils import save_profile_image

users_bp = Blueprint('users', __name__, template_folder='templates')

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash("Реєстрація успішна! Увійдіть у свій акаунт.", "success")
        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form, title="Реєстрація")

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = LoginForm()

    if form.validate_on_submit():
        username_or_email = form.username.data
        password = form.password.data

        stmt = select(User).where(
            (User.username == username_or_email) |
            (User.email == username_or_email)
        )
        user = db.session.scalars(stmt).first()

        if user and user.check_password(password):
            login_user(user, remember=form.remember.data)
            flash("Вхід успішний!", "success")
            return redirect(url_for('users.account'))

        flash("Невірний логін або пароль!", "danger")

    return render_template("users/login.html", form=form, title="Вхід")

@users_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():

        if form.image.data:
            filename = save_profile_image(form.image.data)
            current_user.image = filename

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash("Профіль оновлено!", "success")
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_url = url_for("static", filename=f"images/{current_user.image}")

    return render_template(
        "users/account.html",
        form=form,
        image_url=image_url,
        title="Профіль"
    )

@users_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash("Старий пароль невірний!", "danger")
            return redirect(url_for('users.change_password'))

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Пароль успішно змінено!", "success")
        return redirect(url_for('users.account'))

    return render_template('users/change_password.html', form=form, title="Зміна пароля")

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for('users.login'))

@users_bp.route('/all_users')
@login_required
def all_users():
    users = db.session.scalars(select(User)).all()
    return render_template(
        'users/all_users.html',
        users=users,
        title="Усі користувачі"
    )
