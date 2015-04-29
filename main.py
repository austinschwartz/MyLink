from flask import Flask, render_template, session, redirect, url_for, escape, request, send_from_directory, abort
#from flask.ext.storage.local import LocalStorage
from forms import RegisterForm, LoginForm, EditProfileForm, RequestFriendForm, AcceptDenyForm, CreateCircleForm, PostForm
from models import db, User, Album, Picture, Post, Friend, Circle
import os

app = Flask(__name__, static_url_path='/static')
#app.config['DEFAULT_FILE_STORAGE'] = 'filesystem'
#app.config['UPLOADS_FOLDER'] = os.path.realpath('.') + '/static/'
#app.config['FILE_SYSTEM_STORAGE_FILE_VIEW'] = 'static'
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
        return render_template('403.html'), 403


@app.route('/')
@app.route('/index')
def index():
    if 'email' not in session:
        return login('Please log in first')
    else:
        friends = Friend.query.filter_by(userid = session['id'])
        friendUsers = []
        for friend in friends:
            friendUser = User.query.filter_by(id = friend.friendid).first()
            if friend.state == 'a':
                friendUsers.append(friendUser)
        return render_template('index.html', friends=friendUsers)

## Users
@app.route('/user/<userid>', methods=['GET', 'POST'])
def user(userid):
    if 'email' not in session:
       return render_template('user.html', user = User.query.filter_by(id = userid).first()) 

    form = RequestFriendForm()
    #friends = Friend.query.filter_by(userid = session['id'], state = "a", friendid=userid)

    friends = Friend.query.filter_by(userid = session['id'], friendid = userid).first();
    friendUsers = []
    isFriend = False
    acceptedFriends = False
    if friends is not None:
	if friends.state != 'p' or friends.state != 'r':
	    isFriend = True
	    if friends.state == 'a':
		acceptedFriends = True

    if request.method == 'POST':
	friend_from = Friend.query.filter_by(friendid = userid, userid = session['id']).first()
	friend_to = Friend.query.filter_by(friendid = session['id'], userid = userid).first() 
	if 'submit' in request.form:
	    if friend_from is None and friend_to is None:
	    	fr = Friend(session['id'], userid, 'r')
	    	db.session.add(fr)
	    	fr = Friend(userid, session['id'], 'p')
	    	db.session.add(fr)
            	db.session.commit()
	    	isFriend = True
	if 'remove' in request.form:
	    db.session.delete(friend_from)
	    db.session.delete(friend_to)
	    db.session.commit()
	    acceptedFriends = False
	    isFriend = False
 

    return render_template('user.html', user = User.query.filter_by(id = userid).first(), form=form, isFriend = isFriend, acceptedFriends = acceptedFriends)

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
    form = PostForm()
    return render_template('posts.html', posts = Post.query.all(), title='posts', form=form)

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
	friendid = request.values['hidden']
	friend_from = Friend.query.filter_by(friendid = friendid, userid = sessionid).first()
	friend_to = Friend.query.filter_by(friendid = sessionid, userid = friendid).first() 
	if 'accept' in request.form:
	    friend_from.state = 'a'
	    friend_to.state = 'a'
	elif 'deny' in request.form:
	    friend_from.state = 'd'
	    friend_to.state = 'd'

	db.session.commit()

    return render_template('request.html', form = form, requests = Friend.query.all(), states = Friend.query.all(), userid = sessionid, title='requests')

# Create Circle
@app.route('/createcircle', methods={'GET', 'POST'})
def createcircle():
    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('login'))

    friends = Friend.query.filter_by(userid = session['id'], state='a')

    form = CreateCircleForm(request.values)

    choices = []
    for friend in friends:
	#print User.query.filter_by(id = friend.friendid).first()
	username = User.query.filter_by(id = friend.friendid).first().name
	choices.append((friend.friendid, username))

    form.multiple.choices = choices
    
    if request.method == 'POST':
	name = request.values.get('name')
	multiple = request.values.getlist('multiple')
	maxidtup = db.session.query(db.func.max(Circle.circleid)).first()
	maxid = maxidtup[0]+1
	for friend in multiple:
	    circle = Circle(name, maxid, session['id'], friend)
	    db.session.add(circle)
	db.session.commit()
	return redirect(url_for('circle', circleid = maxid))

    return render_template('createcircle.html', title = 'createcircle', form=form)


# Circle
@app.route('/circle/<circleid>', methods={'GET','POST'})
def circle(circleid):
    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('login'))

    users_in_circle = Circle.query.filter_by(circleid = circleid)
    users = []
    
    for _user in users_in_circle:
	print _user.userid
	users.append(User.query.filter_by(id = _user.userid).first())

    return render_template('circle.html', title = 'circle', users = users)

## Circles
@app.route('/circles', methods={'GET', 'POST'})
def circles():
    if 'email' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('login'))

    friends = Friend.query.filter_by(userid = session['id'], state='a')

    form = CreateCircleForm(request.form)

    circles = Circle.query.group_by(Circle.circleid).filter_by(ownerid = session['id'])

    if request.method == 'POST':
        if 'submit' in request.form:
	    return redirect(url_for('createcircle'))

    return render_template('circles.html', title = "circles", form=form, circles = circles)

## Albums
@app.route('/album/<int:albumid>')
def album(albumid): # no default here, error if there is no albumid
    album = Album.query.filter_by(id = albumid).first()
    ownerid = album.ownerid

    # forbidden if user not logged in and album isnt public
    if 'email' not in session and album.visibility != 'public':
        abort(403)

    # show album is user is owner or public
    if album.visibility == 'public' or ownerid == session['id']: 
        pictures = Picture.query.filter_by(albumid = albumid)
        return render_template('album.html', album = album, pictures = pictures, title='album')
    else:
        abort(403)

@app.route('/albums')
def albums():
    
    return render_template('albums.html', albums = Album.query.all(), title='albums')


## Login/Logout
@app.route('/login', methods=['GET', 'POST'])
def login(error=''):
    form = LoginForm()

    if 'email' in session:
        return redirect(url_for('index'))
    if request.method =='POST':
        if form.validate() == False:
            return render_template('login.html', form=form, title='login', error=error)
        else:
            session['email'] = form.email.data
	    session['id'] =  User.query.filter_by(email = form.email.data).first().id
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('login.html', form=form, title='login', error=error)

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
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload a new file."""
    if request.method == 'POST':
        save(request.files['upload'])
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/images/albums/<int:albumid>/<filename>')
def image(albumid, filename):
    album = Album.query.filter_by(id = albumid).first()
    ownerid = album.ownerid

    # forbidden if user not logged in and album isnt public
    if 'email' not in session and album.visibility != 'public':
        abort(403)

    # show album is user is owner or public
    if album.visibility == 'public' or ownerid == session['id']: 
        return send_from_directory('static/images/albums/' + str(albumid), filename)
    else:
        abort(403)

# Everything else
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(root, path)


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(port = 8080, debug = True)
