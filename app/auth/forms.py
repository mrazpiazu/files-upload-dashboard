from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('Email Address', validators=[Email(), DataRequired(), Length(max=64)])
    first_name = StringField('First name', validators=[Length(min=2, max=100)])
    last_name = StringField('Last name', validators=[Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=64), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the terms and conditions', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[Length(min=6, max=255), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')