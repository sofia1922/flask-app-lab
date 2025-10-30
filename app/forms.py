from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp

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
        validators=[DataRequired(message="Поле обов’язкове!"),
                    Length(min=4, max=10, message="Пароль 4–10 символів")]
    )

    remember = BooleanField("Запам’ятати мене")
    submit = SubmitField("Увійти")