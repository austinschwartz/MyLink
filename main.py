from flask import Flask, render_template, session, redirect, url_for, escape, request, send_from_directory
#from flask.ext.storage.local import LocalStorage
from forms import RegisterForm, LoginForm, EditProfileForm, RequestFriendForm, AcceptDenyForm
from models import db, User, Album, Picture, Post, Friend
import os

app = Flask(__name__, static_url_path='/static')
#app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
#app.config['UPLOADS_FOLDER'] = os.path.realpath('.') + '/static/'
#app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static'
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

@app.route('/')
@app.route('/index')
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        friends = Friend.query.filter_by(userid = session['id'])
        friendUsers = []
        for friend in friends:
            friendUser = User.query.filter_by(id = friend.id).first()
            if friend.state == 'a':
                friendUsers.append(friendUser)
        return render_template('index.html', friends=friendUsers)

## Users
@app.route('/user/<userid>', methods={'GET', 'POST'})
def user(userid):
    if 'email' not in session:
       return render_template('user.html', user = User.query.filter_by(id = userid).first()) 

    form = RequestFriendForm()
    #friends = Friend.query.filter_by(userid = session['id'], state = "a", friendid=userid)

    friends = Friend.query.filter_by(userid = session['id'], friendid = userid)
    friendUsers = []
    isFriend = False
    for friend in friends:
	print "Is Friend"
	isFriend = True

    if request.method == 'POST':
	##print request.form
	if 'submit' in request.form:
	    print "adding friend"
	    fr = Friend(session['id'], userid, 'r')
	    db.session.add(fr)
	    fr = Friend(userid, session['id'], 'p')
	    db.session.add(fr)
            db.session.commit()
	    isFriend = True
	    

    return render_template('user.html', user = User.query.filter_by(id = userid).first(), form=form, isFriend = isFriend)

@app.route('/users')
def users():
    return render_template('users.html', users = User.query.all(), title="users")

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
                return render_template('profile.html', form=form, title='profile')
            else:
                user = User.query.filter_by(email=session['email']).first()
                user.password = form.password.data
                db.session.commit()
            return redirect(url_for('index'))
        user = User.query.filter_by(email=session['email']).first()
        #form.password = user.password

        return render_template('profile.html', form=form, title='profile')
    

## Posts
@app.route('/post/<int:postid>')
def post(postid): # no default here, error if there is no postid
    pass

@app.route('/posts')
def posts():
    return render_template('posts.html', posts = Post.query.all(), title='posts')

##Requests
@app.route('/requests',  methods=['GET','POST'])
def requests():
    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('login'))
    
    form = AcceptDenyForm(request.values)
    
    friends = Friend.query.filter_by(friendid = session['id'])
    friendUsers = []
    for friend in friends:
        friendUser = User.query.filter_by(id = friend.id).first()
        if friend.state == 'p':
            friendUsers.append(friendUser)

    sessionid = session['id']
    if request.method == 'POST':
	if 'accept' in request.form:
	    friend_id = request.values['hidden']
	    acceptdeny(sessionid, friend_id, "p", "r", "a")
	elif 'deny' in request.form:
	    friend_id = request.values['hidden']
	    acceptdeny(sessionid, friend_id, "p", "r", "d")

    return render_template('request.html', form = form, requests = Friend.query.all(), states = Friend.query.all(), userid = session['id'], title='requests')

#accept is (id, id, p, r, a)
def acceptdeny(sessionid, friend_id, state1, state2, state3):
    print "accept deny", sessionid, friend_id, state1, state2, state3
    friends = Friend.query.filter_by(friendid = sessionid)

    for friend in friends:
        print friend
	if str(friend.state) == str(state1) and str(friend.friendid) == str(sessionid) and str(friend.userid) == str(friend_id):
	    friend.state = state3
	    db.session.commit()
      
    friends = Friend.query.filter_by(friendid = friend_id)

    for friend in friends:
	if str(friend.state) == str(state2) and str(friend.userid) == str(sessionid) and str(friend.friendid) == str(friend_id):
	    friend.state = state3
	    db.session.commit()



## Albums
@app.route('/album/<int:albumid>')
def album(albumid): # no default here, error if there is no albumid
    album = Album.query.filter_by(id = albumid).first()
    pictures = Picture.query.filter_by(albumid = albumid)
    return render_template('album.html', album = album, pictures = pictures)

@app.route('/albums')
def albums():
    return render_template('albums.html', albums = Album.query.all(), title='albums')


## Login/Logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if 'email' in session:
        return redirect(url_for('index'))
    if request.method =='POST':
        if form.validate() == False:
            return render_template('login.html', form=form, title='login')
        else:
            session['email'] = form.email.data
	    session['id'] =  User.query.filter_by(email = form.email.data).first().id
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('login.html', form=form, title='login')

@app.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('login'))

    session.pop('email', None)
    session.pop('id', None)
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
	    session['id'] =  User.query.filter_by(email = session['email']).first().id
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('register.html', form = form, title='register')


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
