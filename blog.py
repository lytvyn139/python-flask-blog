from flask import Flask, render_template, redirect, url_for, flash
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask (__name__) #__name__ is name of the module

# secret key will protect against modifying a cookie, for demo case it's open !!!
# for production it must be hidden 
app.config['SECRET_KEY'] = 'any'

# DB
# One to many: One user have many post, but post have only one author

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True ) #primary_key=True unique to each user
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
  password = db.Column(db.String(60), nullable=False) #hashing string will be 60 symb
  #posts - connector to Post model, backref is another column author, lazy loading
  posts = db.relationship('Post', backref='author', lazy=True)

  def __repr__(self): #how object is printed
    return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True ) 
  title = db.Column(db.String(100), nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  content = db.Column(db.Text, nullable=False)
  #adding user.id for the author, relationship to user (lover case table/column name) model db.ForeignKey('user.id')
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

  def __repr__(self): #how object is printed
    return f"Post('{self.title}', '{self.date_posted}')"

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
    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('home'))
  return render_template('register.html', title='Register', form=form) #to pass the from to register.html

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@blog.com' and form.password.data == 'test@blog.com':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# hot reload/debugger is active
if __name__ == '__main__':
  app.run(debug=True)
