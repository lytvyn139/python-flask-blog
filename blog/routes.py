import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from blog.models import User, Post

#two routes leads to home
@app.route("/")
@app.route("/home")
def home():
  posts = Post.query.order_by(Post.date_posted.desc()).all()
  #pagination is not working!
  #page = request.args.get('page', 1, type=int)
  #posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
  return render_template('home.html', posts=posts)

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

def save_picture(form_picture):
  #generate random name for saving
  random_hex = secrets.token_hex(8)
  #making sure we gonna save file with save ext
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  #saving files here
  picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
  #resize image from Pillow
  output_size = (125, 125)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(picture_path)
  return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required #also check __init__.py ln 16
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
        picture_file = save_picture(form.picture.data)
        current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Data has been updated!', 'success')
    return redirect(url_for('account'))
  #this handles form pre-populated with cur values  
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
  return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required 
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(title=form.title.data, content=form.content.data, author=current_user) #author form models.py
    #save to db
    db.session.add(post)
    db.session.commit()
    flash('Post has been created!', 'success')
    return redirect(url_for('home'))
  return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
      #only user created post can change it
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

# THIS LINK WILL SHOW USER POSTS
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@app.errorhandler(404)
def error_404(error):
  return render_template('errors/404.html'), 404

@app.errorhandler(403)
def error_403(error):
  return render_template('errors/403.html'), 403

@app.errorhandler(500)
def error_500(error):
  return render_template('errors/500.html'), 500