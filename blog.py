from flask import Flask, render_template, redirect, url_for, flash
from forms import RegistrationForm, LoginForm

app = Flask (__name__) #__name__ is name of the module

# secret key will protect against modifying a cookie, for demo case it's open !!!
# for production it must be hidden 
app.config['SECRET_KEY'] = 'any'

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
