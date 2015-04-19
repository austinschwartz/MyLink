from flask import Flask, render_template, session, redirect, url_for, escape, request
from forms import RegisterForm, LoginForm
from models import db, User, Album, Picture, Post
import os

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

## Users
@app.route('/user/<userid>')
def user(userid): # we'll let -1 mean the current user
    pass

@app.route('/users')
def users():
    return render_template('users.html', users = User.query.all())

@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('login'))
    else:
        return render_template('profile.html')

## Posts
@app.route('/post/<postid>')
def post(postid): # no default here, error if there is no postid
    pass

@app.route('/posts')
def posts():
    return render_template('posts.html', posts = Post.query.all())

## Albums
@app.route('/album/<albumid>')
def album(albumid): # no default here, error if there is no albumid
    pass

@app.route('/albums')
def albums():
    return render_template('albums.html', albums = Album.query.all())


## Login/Logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if 'email' in session:
        return redirect(url_for('index'))
    if request.method =='POST':
        if form.validate() == False:
            return render_template('login.html', form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('login'))

    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('register.html', form = form)
        else:
            user = User(form.name.data, form.email.data, form.password.data)
            db.session.add(user)
            db.session.commit()
            session['email'] = user.email
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('register.html', form = form)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(port = 8080, debug = True)
