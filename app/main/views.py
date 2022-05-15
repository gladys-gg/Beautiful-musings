from flask import render_template,request,redirect,url_for,abort,url_for,flash
from . import main
from .forms import *
from ..models import *
from .. import bcrypt,db
from flask_login import login_required, current_user

# Views
@main.route('/')
def index():
    name = "Time to get started "
    posts = Post.query.all()
    # context ={
    #     name: name
    # }
    return render_template('index.html', name=name, posts = posts)

@main.route('/signup',methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User (username = form.username.data,
                    email = form.email.data,
                    password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('your account has been created successfully.')
    return render_template('signUp.html', form = form)

@main.route('/signin', methods=['GET','POST'])
@login_required
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    
    return render_template('signIn.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@main.route('/post/new', methods=['GET','POST'])
def new_post():
    form = PostForm()
    
    return render_template('newPost.html', form = form)
@main.route('/post/<int:id>/update', methods=['GET','POST'])
def update_post(id):
    form = UpdatePostForm()
    
    return render_template('updatePost.html', form = form)