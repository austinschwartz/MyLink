from models import db, User, Picture, Album, Session

db.drop_all()
db.create_all()

db.session.add(User("George Foreman", "george@gmail.com", "abc123"))
db.session.add(User("Mary Juana", "mary@gmail.com", "mary123"))
db.session.add(User("Peter", "peter@gmail.com", "peter134"))

db.session.add(Album("album1",'george@gmail.com',"public"))
db.session.add(Album("album1",'george@gmail.com',"public"))
db.session.add(Album("album1",'george@gmail.com',"public"))
db.session.add(Album("album1",'mary@gmail.com',"public"))

db.session.add(Picture("image-89.jpg","album1", 1 ))
db.session.add(Picture("image-90.jpg","album1", 1 ))
db.session.add(Picture("image-91.jpg","album1", 1 ))
db.session.add(Picture("image-92.jpg","album1", 1 ))

db.session.commit()


