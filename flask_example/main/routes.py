from flask import Blueprint, render_template, request
from flask_example.models import Post

main = Blueprint('main', __name__)


@main.route('/home/')
@main.route('/')
def home():  # view for home page
    page = request.args.get('page', 1, type=int)  # get page arg or return 1 if None
    posts = Post.query. \
        order_by(Post.date_posted.desc()). \
        paginate(page=page, per_page=5)
    return render_template('home.html', title='Home', posts=posts)


@main.route('/about/')
def about():  # view for about page
    return render_template('about.html', title='About')
