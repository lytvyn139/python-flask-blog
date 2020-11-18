from flask import render_template, url_for, flash, redirect, request
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
  {
    'author': 'Iurii Lytvyn',
    'title': 'Blog Post 1',
    'content': 'You day of the year',
    'date_posted': 'April 1, 2020'
  },
  {
    'author': 'Johm Smith',
    'title': 'Blog Post 2',
    'content': 'I don\'t know what I\'m doing',
    'date_posted': 'May 2, 2019'
  },
]

#two routes leads to home
@app.route('/') # <-- flask decorators
@app.route('/home')
def home():
  return render_template('home.html', posts=posts) #passing posts dict 

@app.route('/about')
def about():
  return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    #if the password ok then hash pass
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    #save to db
    db.session.add(user)
    db.session.commit()
    flash(f'{form.username.data}, your account has been created !', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form) #to pass the from to register.html

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
      """
        if form.email.data == 'test@blog.com' and form.password.data == 'test@blog.com':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
      """
        #check if user name is in db
      user = User.query.filter_by(email=form.email.data).first()
      #check: if user + password === hashed pass from form db
      if user and bcrypt.check_password_hash(user.password, form.password.data):
        #login user is from models.py "from flask_login import UserMixin"
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('home'))
      else:
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required #also check __init__.py ln 16
def account():
    return render_template('account.html', title='Account')