from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from app.forms import LoginForm, RegisterForm
from app import db
from app.users.models import User
from flask_login import login_user, logout_user, login_required, current_user

users_bp = Blueprint('users', __name__, template_folder='templates')


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash("Реєстрація успішна! Тепер увійдіть у систему.", "success")
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
        else:
            flash("Невірне ім’я користувача або пароль!", "danger")

    return render_template('users/login.html', form=form, title='Вхід')


@users_bp.route('/account')
@login_required
def account():
    return render_template('users/account.html', user=current_user, title="Профіль")


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Ви вийшли із системи", "info")
    return redirect(url_for('users.login'))


@users_bp.route('/all_users')
@login_required
def all_users():
    stmt = select(User)
    users = db.session.scalars(stmt).all()

    return render_template(
        'users/all_users.html',
        users=users,
        title="Усі користувачі"
    )
