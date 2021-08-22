from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={
                        "placeholder": "Title"})
    body = TextAreaField('Post content', validators=[DataRequired()], render_kw={
                         "placeholder": "Post content"})
    is_published = BooleanField('Published')
