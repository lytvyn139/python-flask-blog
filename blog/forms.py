from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField #for user remember

from wtforms.validators import DataRequired #to make sure it's not empty string
from wtforms.validators import Length #self explained
from wtforms.validators import Email #self explained
from wtforms.validators import EqualTo #self explained

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


class LoginForm(FlaskForm):
  email = StringField('Email',
  validators=[DataRequired(), Email()]) #Username label in html

  password = PasswordField('Password',
  validators=[DataRequired()])

  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')
