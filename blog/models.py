from datetime import datetime 
from blog import db


# DB
# One to many: One user have many post, but post have only one author
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