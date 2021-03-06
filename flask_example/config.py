import json
import secrets

try:
    with open('config.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {
        'secret_key': secrets.token_hex(16),
        'uri': 'sqlite:///blog.db',
        'username': 'username@gmail.com',
        'password': 'password'
    }


class Config:
    SECRET_KEY = data['secret_key']  # get secret key
    SQLALCHEMY_DATABASE_URI = data['uri']  # get database's uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # stops the annoying warning when running app
    MAIL_SERVER = 'smtp.googlemail.com'  # this is google's email server
    MAIL_PORT = 587  # emails use 587th port apparently
    MAIL_USE_TLS = True  # TLS for security
    MAIL_USERNAME = data['username']  # retrieve username
    MAIL_PASSWORD = data['password']  # retrieve password
