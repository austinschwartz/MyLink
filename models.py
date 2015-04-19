from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self, name, email, password):
	self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    owner = db.Column(db.Text)
    visibility = db.Column(db.Text)
    #users = db.relationship('users', backref = db.backref('albums', lazy = 'dynamic'))

    def __init__(self, name, owner, visibility):
        self.name=name
	self.owner=owner
	self.visibility=visibility

    def __repr__(self):
	return '<Album %r>' % self.id

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    ownerid = db.Column(db.Integer)
    
    def __init__(self, name, ownerid):
	self.name = name
	self.ownerid = ownerid

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


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Text)
    session = db.Column(db.Text)

    def __init__(self, user, session):
	self.user = user
	self.owner = owner

    def __repr_(self):
	return '<Session %r>' %self.id
