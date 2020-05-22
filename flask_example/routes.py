from flask import render_template, url_for, flash, redirect
from flask_example import app
from flask_example.forms import RegistrationForm, LoginForm
from flask_example.models import User, Post


posts = [
    {
        'author': 'Mihir Shrestha',
        'date_posted': 'January 19, 2020',
        'title': 'First post',
        'content': 'Hello World!'
    },

    {
        'author': 'John Thompson',
        'date_posted': 'January 25, 2020',
        'title': 'Second post',
        'content': 'Lorem Ipsum'
    },
]


@app.route('/home/')
@app.route('/')
def home():
    return render_template('home.html', title='Home', posts=posts)


@app.route('/about/')
def about():
    return render_template('about.html', title='About')


@app.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)