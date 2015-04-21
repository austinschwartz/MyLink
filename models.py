from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


#friend = db.Table('friend', 
#            db.Column('userid', db.Integer, db.ForeignKey('User.id')), 
#            db.Column('friendid', db.Integer, db.ForeignKey('User.id'))
#            )

#request = db.Table('request', 
#            db.Column('userid', db.Integer, db.ForeignKey('User.id')), 
#            db.Column('requestingid', db.Integer, db.ForeignKey('User.id'))
#            )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    picture = db.Column(db.Text)

    friend = db.relationship("Friend", backref="user")

    def __init__(self, name, email, password, picture=""):
	self.name = name
        self.email = email
        self.password = password
        self.picture = picture

    def __repr__(self):
        return '<User %r>' % self.email

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, ForeignKey('user.id'))
    friendid = db.Column(db.Integer)
    state = db.Column(db.Text)

    def __init__(self, userid, friendid, state):
	self.userid = userid
	self.friendid = friendid
	self.state = state

    def __repr__(self):
	return '<Friend %r>' % self.id

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    ownerid = db.Column(db.Text)
    visibility = db.Column(db.Text)
    #users = db.relationship('users', backref = db.backref('albums', lazy = 'dynamic'))

    def __init__(self, name, ownerid, visibility):
        self.name=name
	self.ownerid=ownerid
	self.visibility=visibility

    def __repr__(self):
	return '<Album %r>' % self.id

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.Text)
    albumid = db.Column(db.Integer)

    def __init__(self, filename, albumid):
	self.filename = filename
        self.albumid = albumid

    def __repr__(self):
	return '<Picture %r>' % self.id

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    ownerid = db.Column(db.Integer)
    albumid = db.Column(db.Integer)
    
    def __init__(self, text, ownerid, albumid):
	self.text = text
	self.ownerid = ownerid
	self.albumid = albumid

    def __repr__(self):
	return '<Post %r>' % self.id

class Circle(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    circleid = db.Column(db.Integer)
    ownerid = db.Column(db.Integer)
    userid = db.Column(db.Integer)

    def __init__(self, circleid, ownerid, userid):
	self.userid = userid
	self.ownerid = ownerid
	self.circleid = circleid

    def __repr__(self):
	return '<Circle %r>' % self.id

