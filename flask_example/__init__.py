from flask import Flask  # import flask itself
from flask_sqlalchemy import SQLAlchemy  # import the database package
from flask_bcrypt import Bcrypt  # import encrypt package
from flask_login import LoginManager  # import special login manager
import json
from flask_mail import Mail

with open('config.json', 'r') as f:
    data = json.load(f)

app = Flask(__name__)  # create Flask object
app.config['SECRET_KEY'] = data['secret_key']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)  # create database with Flask object
bcrypt = Bcrypt(app)  # create encryption with Flask object
login_manager = LoginManager(app)  # create login-manager with Flask object
login_manager.login_view = 'login'  # the view for our login page
login_manager.login_message_category = 'info'  # type of bootstrap class we'll use for messages
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'flaskblogexample@gmail.com'
app.config['MAIL_PASSWORD'] = data['password']

from flask_example import routes  # import routes from flask_example package
