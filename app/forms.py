from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SubmitField,
    SelectField, PasswordField, BooleanField
)
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

from app.users.models import User

class ContactForm(FlaskForm):
    name = StringField(
        "Ім’я",
        validators=[DataRequired(), Length(min=4, max=10)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    phone = StringField(
        "Телефон",
        validators=[
            DataRequired(),
            Regexp(r'^\+?\d{10,15}$', message="Невірний формат номера телефону")
        ]
    )

    subject = SelectField(
        "Тема",
        choices=[
            ("знайомство", "Знайомство"),
            ("співпраця", "Співпраця"),
            ("запитання", "Запитання"),
            ("інше", "Інше")
        ],
        validators=[DataRequired()]
    )

    message = TextAreaField(
        "Повідомлення",
        validators=[DataRequired(), Length(min=5, max=500)]
    )

    submit = SubmitField("Відправити")

class LoginForm(FlaskForm):
    username = StringField(
        "Ім’я користувача або Email",
        validators=[DataRequired(message="Поле обов’язкове!")]
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(message="Поле обов’язкове!"),
            Length(min=4, max=10)
        ]
    )

    remember = BooleanField("Запам’ятати мене")
    submit = SubmitField("Увійти")

class RegisterForm(FlaskForm):
    username = StringField(
        "Ім’я користувача",
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=4, max=20)
        ]
    )

    submit = SubmitField("Зареєструватися")

    def validate_username(self, field):
        existing = User.query.filter_by(username=field.data).first()
        if existing:
            raise ValidationError("Такий username вже існує!")

    def validate_email(self, field):
        existing = User.query.filter_by(email=field.data).first()
        if existing:
            raise ValidationError("Цей email вже використовується!")

class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Ім’я користувача",
        validators=[DataRequired(), Length(min=3, max=50)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    about_me = TextAreaField(
        "Про себе",
        validators=[Length(max=500)]
    )

    image = FileField(
        "Фото профілю",
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], "Тільки JPG/PNG!")]
    )

    submit = SubmitField("Оновити")

    def validate_email(self, field):
        if field.data != current_user.email:
            user = User.query.filter_by(email=field.data).first()
            if user:
                raise ValidationError("Цей email уже використовується!")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Старий пароль", validators=[DataRequired()])
    new_password = PasswordField("Новий пароль", validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField("Підтвердження пароля", validators=[DataRequired()])

    submit = SubmitField("Змінити пароль")

    def validate(self):
        rv = super().validate()
        if not rv:
            return False

        if self.new_password.data != self.confirm_password.data:
            self.confirm_password.errors.append("Паролі не співпадають!")
            return False

        return True

class RecipeForm(FlaskForm):
    title = StringField("Назва", validators=[DataRequired(), Length(min=2, max=100)])

    category_id = SelectField(
        "Категорія",
        coerce=int,
        validators=[DataRequired()]
    )

    cook_time = StringField("Час приготування", validators=[DataRequired()])
    ingredients = TextAreaField("Інгредієнти", validators=[DataRequired()])
    instructions = TextAreaField("Інструкції", validators=[DataRequired()])

    image = FileField("Фото", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    submit = SubmitField("Зберегти")
