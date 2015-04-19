from models import db, User, Picture, Album, Session

db.drop_all()
db.create_all()

db.session.add(User("George Zimmerman", "george@gmail.com", "abc123"))
db.session.add(User("Mary Mary", "mary@gmail.com", "mary123"))
db.session.commit()


