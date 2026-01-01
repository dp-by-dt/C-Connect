# File for Authentication classes using CSRF

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FileField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError

from flask_wtf.file import FileAllowed, FileRequired
import re


#helper function to check the password complexity
def password_complexity(form, field):
    pw = field.data or ''
    if len(pw) < 8:
        raise ValidationError('Password must be at least 8 characters.')
    if not re.search(r'\d', pw):
        raise ValidationError('Password must include at least one digit.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', pw):
        raise ValidationError('Password must include at least one symbol.')
    

# user name formatting 
def username_format(form, field):
    username = field.data or ""
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError("Username can contain only letters, numbers, and underscores.")




class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30),username_format])
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
    username = StringField('Username', validators=[Optional(), Length(min=2, max=30),username_format])
    department = StringField('Department', validators=[Optional(), Length(max=120)])
    year = StringField('Year', validators=[Optional(), Length(max=20)])  # Use SelectField if you want fixed choices
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=1000)])
    interests = StringField('Interests', validators=[Optional(), Length(max=500)])  # comma-separated input
    location = StringField('Location', validators=[Optional(), Length(max=200)])
    profile_picture = FileField('Profile Picture', validators=[
        Optional(),
        FileAllowed({'png', 'jpg', 'jpeg', 'webp'}, 'jpg, png or webp only!')
    ])
    submit = SubmitField('Save')



#-------------- Forget password seciton -------------
class ForgotPasswordForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField("Send reset link")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[DataRequired(), Length(min=8)]
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[EqualTo('password')]
    )
    submit = SubmitField("Reset Password")




# ---------- Change Password Section ------------

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired()]
    )
    new_password = PasswordField(
        "New Password",
        validators=[DataRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[EqualTo("new_password")]
    )
    submit = SubmitField("Change Password")
