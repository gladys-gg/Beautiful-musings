from flask import render_template,request,redirect,url_for,abort,url_for,flash
from . import main
from .forms import *
from ..models import *
from .. import bcrypt,db
from flask_login import login_required, current_user, login_user,logout_user

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
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    
    return render_template('signIn.html', form = form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('newPost.html', form = form)
@main.route('/post/<int:id>/update', methods=['GET','POST'])
def update_post(id):
    form = UpdatePostForm()
    
    return render_template('updatePost.html', form = form)

@main.route('/pitch/new', methods=['GET', 'POST'])
@login_required
def newpitch():
    
    return render_template('newpitch.html', form= form, legend='New Post')


@main.route('/comment/<int:post_id>',methods = ['POST','GET'])
@login_required
def comment(pitch_id):
    post=Post.query.get_or_404(post_id)
    form = CommentForm()
    allComments = Comment.query.filter_by(post_id = post_id).all()
    if form.validate_on_submit():
        postedComment = Comment(comment=form.comment.data,user_id = current_user.id, post_id = post_id)
        post_id = post_id
        db.session.add(postedComment)
        db.session.commit()
        flash('Comment added successfully')
        
        return redirect(url_for('main.comment',pitch_id=pitch_id))

    return render_template("comment.html",pitch=pitch, title='Say something about this post', form = form,allComments=allComments)

@main.route('/delete/comment/<comment_id>')
@login_required

def deleteComment(comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first()

    if not comment:
        flash('Comment not found', category='error')
    elif current_user.id != comment.user.id and  current_user.id != post.author.id:
        flash('YOu are not authorized to delete this comment', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('main.index'))