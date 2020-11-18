# Flask blog

Flask blog pet project

## Stack used

Python + Flask (Jinja2, SQLAlchemy, Forms) + Bootstrap

## Populate db +

```cs
python
from blog import db
db.create_all()
from blog.models import User, Post
user_1 = User(username='Root', email='Root@gmail.com', password='11111')
db.session.add(user_1)

user_2 = User(username='Sam', email='Sam@gmail.com', password='22222')
db.session.add(user_2)
db.session.commit()
```

## Queries

```cs
User.query.all()
User.query.first()
User.query.filter_by(username='Root').all()
root = User.query.filter_by(username='Root').first()
root.id
user = User.query.get(1)
user
user.posts
post_1 = Post(title='Test post 1', content='my content', user_id=user.id)
post_2 = Post(title='Test post 2', content='my content second', user_id=user.id)
db.session.add(post_1)
db.session.add(post_2)
user.posts
for post in user.posts:
  print(post.title)

post = Post.query.first()
post
post.user_id
post.author

db.drop_all()
```

## Installation

```cs
python3 -m venv py3Env
source py3Env/bin/activate
pip3 install -r requirements.txt
#pip3 install flask flask_sqlalchemy flask_wtf email_validator
#pip3 freeze > requirements.txt

python run.py

```

## Author

IURII LYTVYN

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Screenshot
