from flask_wtf import FlaskForm
from blog.models import User

from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField #for user remember

from wtforms.validators import DataRequired 
from wtforms.validators import Length 
from wtforms.validators import Email 
from wtforms.validators import EqualTo 
from wtforms.validators import ValidationError 

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


class LoginForm(FlaskForm):
  email = StringField('Email',
  validators=[DataRequired(), Email()]) #Username label in html
  password = PasswordField('Password',
  validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')
