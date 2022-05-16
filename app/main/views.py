from PIL import Image
from flask import render_template,request,redirect,url_for,abort,url_for,flash
from . import main
from .forms import *
from ..models import *
from .. import bcrypt,db
from flask_login import login_required, current_user, login_user,logout_user
from ..request import get_random_quote


# Views
@main.route('/')
def index():
    name = "Time to get started "
    posts = Post.query.all()
    quote = get_random_quote()

    return render_template('index.html', name=name, posts = posts, quote = quote)


@main.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email = form.email.data, username = form.username.data,password = hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('signUp.html',form = form)

@main.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid')
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
@main.route('/post/<int:post_id>/update', methods=['GET','POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.new_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('updatePost.html', form = form)


@main.route('/comment/<int:post_id>',methods = ['POST','GET'])
@login_required
def comment(post_id):
    post=Post.query.get_or_404(post_id)
    form = CommentForm()
    allComments = Comment.query.filter_by(post_id = post_id).all()
    if form.validate_on_submit():
        postedComment = Comment(comment=form.comment.data,user_id = current_user.id, post_id = post_id)
        post_id = post_id
        db.session.add(postedComment)
        db.session.commit()
        flash('Comment added successfully')
        
        return redirect(url_for('main.comment',post_id=post_id))

    return render_template("comment.html",post=post, title='Say something about this post', form = form,allComments=allComments)

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

@main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.','success')
        return redirect(url_for('main.account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form = form)