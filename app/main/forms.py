from flask_wtf import FlaskForm
from wtforms import Form,StringField, TextAreaField, SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo, ValidationError
from app.models import *

class RegistrationForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password: ', validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(),EqualTo('password')])
    
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. PLease choose a different one.')
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. PLease choose a different one.')

    
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Sign In')
    
class PostForm(FlaskForm):
    title = StringField('The Title:', validators = [DataRequired()])
    content = TextAreaField('Your Content', validators = [DataRequired()])
    submit = SubmitField('Post')
    
class UpdatePostForm(FlaskForm):
    title = StringField('The Title:', validators = [DataRequired()])
    content = TextAreaField('Your Content', validators = [DataRequired()])
    submit = SubmitField('Update Post')
    
class CommentForm(FlaskForm):
    comment = TextAreaField('Say something', validators = [DataRequired()])
    submit = SubmitField('Comment')
    
        