from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField, DateTimeField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from datetime import datetime
from app.users.models import User

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    content = TextAreaField("Content", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[
            ("news", "News"),
            ("publication", "Publication"),
            ("tech", "Tech"),
            ("other", "Other")
        ],
        default="news"
    )
    is_active = BooleanField("Active", default=True)
    publish_date = DateTimeField("Publish Date", default=datetime.utcnow)

    author_id = SelectField("Author", coerce=int)
    tags = SelectMultipleField("Tags", coerce=int)

    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from app.posts.models import Tag

        self.author_id.choices = [(u.id, u.username) for u in User.query.all()]
        self.tags.choices = [(t.id, t.name) for t in Tag.query.all()]
