from flask import (Blueprint, redirect, render_template,
                   url_for, flash, abort, request)
from flask_login import login_required, current_user
from flask_example import db
from flask_example.models import Post
from flask_example.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@login_required
@posts.route("/post/new", methods=['POST', 'GET'])
def new_post():
    if current_user.is_anonymous:
        flash("You must log in to create a post.", 'info')
        return redirect(url_for('users.login'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created successfully!", 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@login_required
@posts.route("/post/<int:post_id>/update", methods=['POST', 'GET'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Edit Post', form=form, legend="Update Post")


@login_required
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted.", 'success')
    return redirect(url_for('main.home'))
