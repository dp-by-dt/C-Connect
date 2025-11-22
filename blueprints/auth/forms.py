# File for Authentication classes using CSRF

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

import re
from wtforms.validators import ValidationError

#helper function to check the password complexity
def password_complexity(form, field):
    pw = field.data or ''
    if len(pw) < 8:
        raise ValidationError('Password must be at least 8 characters.')
    if not re.search(r'\d', pw):
        raise ValidationError('Password must include at least one digit.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', pw):
        raise ValidationError('Password must include at least one symbol.')



class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), password_complexity])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')



class EditProfileForm(FlaskForm):
    #add fields later
    pass