from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_example import db, bcrypt
from flask_example.models import User, Post
from flask_example.users.utils import save_picture, send_reset_email, delete_picture
from flask_example.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                       RequestResetForm, ResetPasswordForm)

users = Blueprint('users', __name__)


@users.route('/register/', methods=['POST', 'GET'])
def register():  # view for register page
    if current_user.is_authenticated:  # if already logged in, redirect to home page
        return redirect(url_for('main.home'))
    form = RegistrationForm()  # get RegistrationForm from flask_example.forms
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account successfully created for {form.username.data}! You can now login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@users.route('/login/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", 'info')
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login unsuccessful. Please check email and password.', 'danger')
    return render_template('users/login.html', title='Login', form=form)


@users.route('/logout/')
def logout():
    logout_user()
    flash("You have logged out successfully.", 'info')
    return redirect(url_for('main.home'))


@login_required
@users.route('/account/', methods=['POST', 'GET'])
def account():
    if current_user.is_anonymous:
        flash("You must log in to view account details.", 'info')
        return redirect(url_for('users.login'))
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            if current_user.image_file != 'default.jpg':
                delete_picture(current_user.image_file)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('users/account.html', title='Account', image_file=image_file, form=form)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)  # get page or first page if None
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('users/user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        flash("You are already logged in.", 'info')
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset/reset_request.html', title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        flash("You are already logged in.", 'info')
    user = User.verify_reset_token(token)
    if not user:
        flash("That is an invalid or expired token.", 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset/reset_token.html', title="Reset Password", form=form)
