from flask import Flask, render_template, session, redirect, url_for, escape, request
from models import db, User, Album, Picture, Post
import os

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    if 'username' in session: # user is logged in
        return render_template('index.html', user = session['username'])
    else:
        return render_template('index.html')

## Users
@app.route('/user/<userid>')
@app.route('/user')
def user(userid=-1): # we'll let -1 mean the current user
    pass

@app.route('/users')
def users():
    return render_template('users.html', users = User.query.all())


## Posts
@app.route('/post/<postid>')
def post(postid): # no default here, error if there is no postid
    pass


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
    if request.method =='POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html', title='Login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(port = 8080, debug = True)
