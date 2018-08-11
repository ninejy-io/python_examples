from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    user = StringField('user', validators=[DataRequired()])
    pwd = PasswordField('pwd', validators=[DataRequired()])
    remember_me = BooleanField('remember', default=False)
    submit = SubmitField('Submit')
