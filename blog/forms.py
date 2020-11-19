from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from blog.models import User

# REGISTRATION 
class RegistrationForm(FlaskForm):
  username = StringField('Username', #Username label in html
  validators=[DataRequired(), Length(min=2, max=20)]) 
  email = StringField('Email',
  validators=[DataRequired(), Email()]) #Username label in html
  password = PasswordField('Password',
  validators=[DataRequired(),  Length(min=6)])
  confirm_password = PasswordField('Confirm Password',
  validators=[DataRequired(),  EqualTo('password')])
  submit = SubmitField('Sign Up')

  # if user is already in db
  def validate_username(self, username):
      user = User.query.filter_by(username=username.data).first()
      if user:
          raise ValidationError('That username is taken. Please choose a different one.')

# if email is already in db
  def validate_email(self, email):
      user = User.query.filter_by(email=email.data).first()
      if user:
          raise ValidationError('That email is taken. Please choose a different one.')

# LOGIN
class LoginForm(FlaskForm):
  email = StringField('Email',
  validators=[DataRequired(), Email()]) #Username label in html
  password = PasswordField('Password',
  validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

# UPDATE
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

# POST
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')