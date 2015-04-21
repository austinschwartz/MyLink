from flask import Flask, render_template, session, redirect, url_for, escape, request, send_from_directory
from flask.ext.storage.local import LocalStorage
from forms import RegisterForm, LoginForm, EditProfileForm, UsersForm
from models import db, User, Album, Picture, Post, Friend
import os


app = Flask(__name__, static_url_path='/static')
app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
app.config['UPLOADS_FOLDER'] = os.path.realpath('.') + '/static/'
app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static'
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

@app.route('/')
@app.route('/index')
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('index.html')

## Users
@app.route('/user/<userid>')
def user(userid): # we'll let -1 mean the current user
    if 'id' not in session:
       return render_template('user.html', user = User.query.filter_by(id = userid).first()) 

    form = UsersForm()
    currentuser = session['id']
    friends = Friend.query.filter_by(userid = currentuser, friendid = userid)
    return render_template('user.html', user = User.query.filter_by(id = userid).first(), form=form)

@app.route('/users')
def users():
    return render_template('users.html', users = User.query.all())

@app.route('/profile', methods=['GET','POST'])
def profile():
    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('login'))
    else:
        form = EditProfileForm()
        if request.method == 'POST':
            if form.validate() == False:
                return render_template('profile.html', form=form)
            else:
                user = User.query.filter_by(email=session['email']).first()
                user.password = form.password.data
                db.session.commit()
            return redirect(url_for('index'))
        user = User.query.filter_by(email=session['email']).first()
        #form.password = user.password
        return render_template('profile.html', form=form)
    

## Posts
@app.route('/post/<int:postid>')
def post(postid): # no default here, error if there is no postid
    pass

@app.route('/posts')
def posts():
    return render_template('posts.html', posts = Post.query.all())


## Albums
@app.route('/album/<int:albumid>')
def album(albumid): # no default here, error if there is no albumid
    album = Album.query.filter_by(id = albumid).first()
    pictures = Picture.query.filter_by(albumid = albumid)
    return render_template('album.html', album = album, pictures = pictures)

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
	    session['id'] =  User.query.filter_by(email = form.email.data).first().id
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


## Files
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(root, path)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload a new file."""
    if request.method == 'POST':
        save(request.files['upload'])
        return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(port = 8080, debug = True)
