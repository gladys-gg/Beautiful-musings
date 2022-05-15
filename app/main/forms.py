from flask_wtf import FlaskForm
from wtforms import Form,StringField, TextAreaField, SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password: ', validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(),EqualTo('password')])
    
    submit = SubmitField('Sign Up')
    
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Sign In')
        