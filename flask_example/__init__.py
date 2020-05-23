from flask import Flask  # import flask itself
from flask_sqlalchemy import SQLAlchemy  # import the database package
from flask_bcrypt import Bcrypt  # import encrypt package
from flask_login import LoginManager  # import special login manager

app = Flask(__name__)  # create Flask object
app.config['SECRET_KEY'] = '015a3921e25e447c5bb42b0202101a94'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)  # create database with Flask object
bcrypt = Bcrypt(app)  # create encryption with Flask object
login_manager = LoginManager(app)  # create login-manager with Flask object
login_manager.login_view = 'login'  # the view for our login page
login_manager.login_message_category = 'info'  # type of bootstrap class we'll use for messages

from flask_example import routes  # import routes from flask_example package
