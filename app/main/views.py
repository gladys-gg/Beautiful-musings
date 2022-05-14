from flask import render_template,request,redirect,url_for
from . import main
from .forms import *

# Views
@main.route('/')
def index():
    name = "Time to get started "
    # context ={
    #     name: name
    # }
    return render_template('index.html', name=name)

@main.route('/signup',methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    
    return render_template('signUp.html', form = form)