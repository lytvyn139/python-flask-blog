from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# secret key will protect against modifying a cookie, for demo case it's open !!!
# for production it must be hidden 

app.config['SECRET_KEY'] = 'any'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

from blog import routes