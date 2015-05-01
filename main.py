from flask import Flask, render_template, session, redirect, url_for, escape, request, send_from_directory, abort
from flask.ext.mail import Message, Mail
#from flask.ext.storage.local import LocalStorage
from forms import RegisterForm, LoginForm, EditProfileForm, RequestFriendForm, AcceptDenyForm, CreateCircleForm, PostForm, DeleteCircleForm, AddFriendToCircleForm
from models import db, User, Album, Picture, Post, Friend, Circle
import os
import datetime
from operator import attrgetter
from werkzeug import secure_filename
from itsdangerous import URLSafeTimedSerializer
import smtplib

app = Flask(__name__, static_url_path='/static')

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
UPLOAD_FOLDER = os.path.join(root, 'images')

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL= True,
    MAIL_USERNAME = 'mylink321@gmail.com',
    MAIL_PASSWORD = 'thisworks'
)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer('mylink')
    return serializer.dumps(email, salt = 'mylink+')

def confirm_token(token, expiration=6400):
    serializer = URLSafeTimedSerializer('mylink')
    try:
        email = serializer.loads( token, salt = 'mylink+', max_age = expiration)
    except:
	return False
    
    return email

def send_email(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender="mylink321@gmail.com")
    mail = Mail(app)
    mail.send(msg)

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
        return render_template('403.html'), 403


@app.route('/')
def blank():
    return index()

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'email' not in session:
        return login('Please log in')
    if session['verify'] == "False":
	return redirect(url_for('verify'))
    else:
        friends = Friend.query.filter_by(userid = session['id'])
        friendUsers = []
        for friend in friends:
            friendUser = User.query.filter_by(id = friend.friendid).first()
            if friend.state == 'a':
                friendUsers.append(friendUser)
        
        circles = Circle.query.filter_by(userid = session['id']).group_by(Circle.circleid)
        
        owncircles = Circle.query.filter_by(ownerid = session['id']).group_by(Circle.circleid)

        posts = db.session.query(Post, Circle).\
                filter(Post.circleid == Circle.circleid).\
                filter(Circle.userid == session['id']).\
                group_by(Post.id).all()
        
        allFriendPosts = db.session.query(Post, Friend).\
                filter(Post.ownerid == Friend.friendid).\
                filter(Friend.userid == session['id']).all()
        
        usersPosts = Post.query.filter_by(ownerid = session['id']).all()
        
        allPosts = []
        for post in posts:
            for thing in post:
                if isinstance(thing, Post):
                    allPosts.append(thing)
        
        for allFriendPost in allFriendPosts:
            for thing in allFriendPost:
                if isinstance(thing, Post):
                    allPosts.append(thing)
        
        for usersPost in usersPosts:
            allPosts.append(usersPost)
    
        allPosts = list(set(allPosts))
        sorted(allPosts, key=attrgetter('createdate'))
        for podst in allPosts:
            print podst.text

        form = PostForm(request.values)

        choices = []
        for circle in owncircles:
            choices.append((circle.circleid, circle.circlename))
        
        ownalbums = Album.query.filter_by(ownerid = session['id']).all()

        userAlbums = []
        userAlbums.append((-1, "No Album"))
        for album in ownalbums:
            userAlbums.append((album.id, album.name))
        
        form.multiple.choices = choices

        if request.method == 'POST':
            fileFound = False
            aid = -1
            files = request.files.getlist('files')
            if files[0]:
                fileFound = True
                a = Album("name", session['id'])
                db.session.add(a)
                db.session.commit()
                album = db.session.query(Album).order_by(Album.id.desc()).first()
                aid = album.id

                for file in files:
                    filename = secure_filename(file.filename)
                    dirpath = os.path.join(UPLOAD_FOLDER, 'albums/' + str(aid))
                    try:
                        os.mkdir(dirpath)
                    except:
                        pass
                    file.save(os.path.join(dirpath, filename))
                    p = Picture(filename, aid)
                    db.session.add(p)
                db.session.commit()
            posttext = form.textbox.data
            form.textbox.data = ""
            multiple = request.values.getlist('multiple')
            
            if len(multiple) == 0: # add to all friends
                post = Post(posttext, session['id'], aid, -1, datetime.datetime.now())
                db.session.add(post)
                db.session.commit()
                post = db.session.query(Post).order_by(Post.id.desc()).first()
                allPosts.append(post)
            currenttime = datetime.datetime.now()
            for cid in multiple:
                post = Post(posttext, session['id'], aid, int(cid), currenttime)
                db.session.add(post)
                db.session.commit()
                post = db.session.query(Post).order_by(Post.id.desc()).first()
                allPosts.append(post)
            db.session.commit()

        users = User.query.order_by(User.id).all()
        albums = Album.query.order_by(Album.id).all()
        pictures = Picture.query.order_by(Picture.id).all()
        friendModels = Friend.query.all()
        friendList = []
        for friend in friendModels:
            if friend.userid == session['id'] and friend.state == 'a':
                friendList.append(int(friend.id))
        friendList.append(int(session['id']))

        return render_template('index.html', 
                friends = friendUsers, 
                owncircles = owncircles, 
                circles = circles, 
                posts = allPosts,
                users = users,
                albums = albums,
                pictures = pictures,
                friendList = friendList,
                form = form)

## Users
@app.route('/user/<userid>', methods=['GET', 'POST'])
def user(userid):
    if 'email' not in session:
       return render_template('user.html', user = User.query.filter_by(id = userid).first()) 
    if session['verify'] == "False":
	return redirect(url_for('verify'))

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
 

    return render_template('user.html', user = User.query.filter_by(id = userid).first(), form=form, isFriend = isFriend, acceptedFriends = acceptedFriends, sessionid = session['id'])

@app.route('/users')
def users():
    if 'email' not in session:
        return login("Please log in")
    if session['verify'] == "False":
	return redirect(url_for('verify'))

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
                return render_template('profile.html', form=form, title='profile', user=user)
            elif form.submit.data is True:
                user = User.query.filter_by(email=session['email']).first()
                if len(form.password.data) > 0:
                    user.password = form.password.data
                user.name = form.name.data
                db.session.commit()
	    elif form.verify.data is True:
		token = generate_confirmation_token(session['email'])
                confirm_url = url_for('confirm', token=token, _external=True)
    		html = render_template('confirm.html', confirm_url=confirm_url)
		subject = "Mylink: confirm email"
		send_email(session['email'], subject, html)
		return render_template('verificationsent.html')

            return redirect(url_for('index'))
        user = User.query.filter_by(email=session['email']).first()

        return render_template('profile.html', form=form, title='profile', user=user)
    
## verify
@app.route('/verify')
def verify():
    return render_template('verify.html', title='verify')

## verify with token
@app.route('/confirm/<token>')
def confirm(token):
    try:
	email = confirm_token(token)
    except:
	flash('verification is invalid')
	return redirect(url_for('profile'))
    
    user = User.query.filter_by(id=session['id']).first()
    user.verified = "True"
    db.session.commit()   
    session['verify']="True"
    return render_template('thankyou.html')


    
## Posts
@app.route('/posts')
def posts():
    if 'email' not in session:
        return login("Please log in")
        return redirect(url_for('login')) 
    if session['verify'] == "False":
	return redirect(url_for('verify'))

    form = PostForm()
    return render_template('posts.html', posts = Post.query.all(), title='posts', form=form)

##Requests
@app.route('/requests',  methods=['GET','POST'])
def requests():
    if 'email' not in session:
        return login("Please log in")
    if session['verify'] == "False":
	return redirect(url_for('verify'))

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
        return login('Please log in first')
    if session['verify'] == "False":
	return redirect(url_for('verify'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('login'))

    friends = Friend.query.filter_by(userid = session['id'], state='a')

    form = CreateCircleForm(request.values)

    choices = []

    for friend in friends:
	#print User.query.filter_by(id = friend.friendid).first()
	username = User.query.filter_by(id = friend.friendid).first().name
	choices.append((str(friend.friendid), username))

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
        return login('Please log in first')

    if session['verify'] == "False":
	return redirect(url_for('verify'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('login'), error='Please log in')

    form = AddFriendToCircleForm()

    users = []
    friendslist = []
    
    circle = Circle.query.group_by(Circle.circleid).filter_by(circleid = circleid, ownerid = session['id']).first()

    friends = Friend.query.filter_by(userid = session['id'], state='a')
    userids = []
    data = []
    
    for friend in friends:
	user = User.query.filter_by(id = friend.friendid).first()
	username = user.name
	userid = user.id
	if userid in users:
	    friendslist.append((userid, username))
	else:
	    friendslist.append((userid, username))
   
    form.checkbox.choices = friendslist

    users_in_circle = Circle.query.filter_by(circleid = circleid)



    if request.method == 'POST':
	if 'submit' in request.form:
	    print form.checkbox.data
	    for box in form.checkbox.data:
		query = Circle.query.filter_by(circleid=circleid, ownerid=session['id'], userid=box).first()
		if query is None:
		    circle = Circle(circle.circlename, circleid, session['id'], box)
		    db.session.add(circle)
		    db.session.commit()
	    users_in_circle = Circle.query.filter_by(circleid = circleid)
	    for u in users_in_circle:
		if unicode(u.userid) not in form.checkbox.data:
		    db.session.delete(u)
		    db.session.commit()
	    
	    #if query is not None:
		    #if query.userid not in form.checkbox.data:
		#	db.session.delete(query)
	     #db.session.commit()
    
    users_in_circle = Circle.query.filter_by(circleid = circleid)

    for _user in users_in_circle:
	dataid = User.query.filter_by(id = _user.userid).first().id
	data.append(unicode(dataid))

    form.checkbox.data = data
    return render_template('circle.html', title = 'circle', form = form, circleid = circleid, friendslist = friendslist, circle = circle)

## Circles
@app.route('/circles', methods=['GET', 'POST'])
def circles():
    if 'email' not in session:
        return login( error='Please log in')
    if session['verify'] == "False":
	return redirect(url_for('verify'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('login'))

    friends = Friend.query.filter_by(userid = session['id'], state='a')

    form = CreateCircleForm(request.form)
    delete_circle_form = DeleteCircleForm(request.values)

    circles = Circle.query.group_by(Circle.circleid).filter_by(ownerid = session['id'])

    if request.method == 'POST':
        if 'submit' in request.form:
	    return redirect(url_for('createcircle'))
	elif 'hidden' in request.form:
	    del_circleid = request.values['hidden']
	    del_circles = Circle.query.filter_by(circleid = del_circleid)
	    for del_circle in del_circles:
		db.session.delete(del_circle)
		db.session.commit()
		circles = Circle.query.group_by(Circle.circleid).filter_by(ownerid = session['id'])

    return render_template('circles.html', title = "circles", form=form, delete_circle_form = delete_circle_form, circles = circles)

## Albums
@app.route('/album/<int:albumid>')
def album(albumid): # no default here, error if there is no albumid
    album = Album.query.filter_by(id = albumid).first()
    ownerid = album.ownerid

    # forbidden if user not logged in and album isnt public
    if 'email' not in session:
        abort(403)

    # show album is user is owner or public
    if ownerid == session['id']: 
        pictures = Picture.query.filter_by(albumid = albumid)
        return render_template('album.html', album = album, pictures = pictures, title='album')
    else:
        abort(403)

@app.route('/albums')
def albums():
    if session['verify'] == "False":
	return redirect(url_for('verify'))

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
	    session['verify'] = User.query.filter_by(email = form.email.data).first().verified
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('login.html', form=form, title='login', error=error)

@app.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('login'))

    session.pop('email', None)
    session.pop('id', None)
    session.pop('verify',None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('register.html', form = form)
        else:
            user = User(form.name.data, form.email.data, form.password.data, 'False')
            db.session.add(user)
            db.session.commit()
            session['email'] = user.email
	    session['id'] =  User.query.filter_by(email = session['email']).first().id
	    session['verify'] = user.verified
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
    if 'email' not in session:
        abort(403)

    return send_from_directory('static/images/albums/' + str(albumid), filename)

# Everything else
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(root, path)


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(port = 8080, debug = True)
