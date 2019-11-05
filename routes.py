import secrets
import os
from app import app, db, bcrypt
from connection import User, Post
from flask import render_template, flash, redirect, url_for, request
from forms import User_Login, User_Registration, Update_acc_info, NewPost
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = User_Login()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.stay_logged.data)
                flash('successful login', 'success')
                nPage = request.args.get('next')
                return redirect(nPage) if nPage else redirect(url_for('home'))
            else:
                flash('invalid login', 'warning')
                return render_template('/login.html', title='Login', form=form)
    else:
        return render_template('/login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = User_Registration()
    if form.validate_on_submit():
        ash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User()
        user.user = form.names.data,
        user.username = form.username.data,
        user.email = form.email.data,
        user.password = ash
        db.session.add(user)
        db.session.commit()
        flash('Account successfully created! ', 'success')
        return redirect(url_for('login'))
    return render_template('/register.html', title='register', form=form)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    posts = Post.query.all()
    return render_template('/home.html', title='home', posts=posts)


def save_image(form_picture):
    random = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random + f_ext
    picture_path = os.path.join(app.root_path,  'static/images' + picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = Update_acc_info()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_image(form.picture.data)
            current_user.image = picture_file
        current_user.user = form.names.data
        current_user.username = form.username.data
        db.session.add(current_user)
        db.session.commit()
        flash('account successfully updated')
        return redirect(url_for('account'))
    elif request.method == 'GET':

        form.names.data = current_user.user
        form.username.data = current_user.username
    image = url_for('static', filename='images/' + current_user.image)
    return render_template(
                            '/my_account.html',
                            title='my_account',
                            image=image, form=form
                        )


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPost()
    if form.validate_on_submit():
        posts = Post(
            title=form.title.data,
            content=form.post.data,
            author=current_user
        )
        db.session.add(posts)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('/create_post.html', title='New post', form=form)


@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    posted = Post.query.get_or_404(post_id)
    return render_template('/post.html', title=posted.title, post=posted)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('/index.html')
