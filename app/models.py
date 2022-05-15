from datetime import datetime
from flask_login import UserMixin
from . import login_manager,db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#user model
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    image_file = db.Column(db.String(100), default='default.jpg')
    password = db.Column(db.String(),nullable=False)
    bio = db.Column(db.String(255),nullable=False)
    posts = db.relationship('Post', backref='author',lazy=True) #defining the one to many relationship btn pitch and author
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    likes =  db.relationship('Like',backref='user',lazy='dynamic')
    dislikes =  db.relationship('Dislike',backref='user',lazy='dynamic')


    def __repr__(self):
        return f'User({self.username},{self.email},{self.image})'


#class Post
class Post (db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False) #Id of the post author
    comment =  db.relationship('Comment',backref='post',lazy='dynamic')
    likes =  db.relationship('Like',backref='post',lazy='dynamic')
    dislikes =  db.relationship('Dislike',backref='post',lazy='dynamic')



def __repr__(self):
    return f"User({self.content},{self.datePosted})"

#comment model
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False) 
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),nullable=False)
    comment = db.Column(db.String(250))

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False) #Id of the user
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),nullable=False)


class Dislike(db.Model):
    __tablename__ = 'dislikes'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False) #Id of the user
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),nullable=False)


def __repr__(self):
    return f'User({self.comment})'


class Quote:

    def __init__(self, author, quote):
        self.author = author
        self.quote = quote