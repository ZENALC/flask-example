from flask import Flask  # import flask itself
from flask_sqlalchemy import SQLAlchemy  # import the database package
from flask_bcrypt import Bcrypt  # import encrypt package
from flask_login import LoginManager  # import special login manager
from flask_mail import Mail  # import mail package
from flask_example.config import Config  # import Configurator


db = SQLAlchemy()  # create database with Flask object
bcrypt = Bcrypt()  # create encryption with Flask object
login_manager = LoginManager()  # create login-manager with Flask object
login_manager.login_view = 'users.login'  # the view for our login page
login_manager.login_message_category = 'info'  # type of bootstrap class we'll use for messages
mail = Mail()  # create mail with Flask object


def create_app(config_class=Config):
    app = Flask(__name__)  # create Flask object
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flask_example.users.routes import users
    from flask_example.posts.routes import posts
    from flask_example.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app


