from flask import render_template, url_for, flash, redirect, request
from flask_example import app, db, bcrypt
from flask_example.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_example.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image


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
def home():  # view for home page
    return render_template('home.html', title='Home', posts=posts)


@app.route('/about/')
def about():  # view for about page
    return render_template('about.html', title='About')


@app.route('/register/', methods=['POST', 'GET'])
def register():  # view for register page
    if current_user.is_authenticated:  # if already logged in, redirect to home page
        return redirect(url_for('home'))
    form = RegistrationForm()  # get RegistrationForm from flask_example.forms
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account successfully created for {form.username.data}! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account/', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)
