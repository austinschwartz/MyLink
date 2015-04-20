from models import db, User, Picture, Album, Session, Post

db.drop_all()
db.create_all()

db.session.add(User("George Foreman", "george@gmail.com", "abc123"))
db.session.add(User("Mary Juana", "mary@gmail.com", "mary123"))
db.session.add(User("Peter", "peter@gmail.com", "peter134"))

db.session.add(Album("album1",1,"public"))
db.session.add(Album("album2",1,"public"))
db.session.add(Album("album3",1,"private"))
db.session.add(Album("album1",2,"public"))
db.session.add(Album("Pictures of my dumb cat",3,"public"))

db.session.add(Picture("image-89.jpg", 1 ))
db.session.add(Picture("image-90.jpg", 1 ))
db.session.add(Picture("image-91.jpg", 1 ))
db.session.add(Picture("image-92.jpg", 1 ))
db.session.add(Picture("image-93.jpg", 2 ))
db.session.add(Picture("image-94.jpg", 2 ))
db.session.add(Picture("image-95.jpg", 2 ))
db.session.add(Picture("image-96.jpg", 2 ))
db.session.add(Picture("image-97.jpg", 2 ))
db.session.add(Picture("image-98.jpg", 2 ))
db.session.add(Picture("image-99.jpg", 2 ))
db.session.add(Picture("image-100.jpg", 2 ))
db.session.add(Picture("image-101.jpg", 3 ))
db.session.add(Picture("image-102.jpg", 3 ))
db.session.add(Picture("image-103.jpg", 4 ))
db.session.add(Picture("image-104.jpg", 5 ))
db.session.add(Picture("image-105.jpg", 5 ))
db.session.add(Picture("image-106.jpg", 5 ))

db.session.add(Post("Today I ate something, pictures enclosed", 1, 1))
db.session.add(Post("Life is pain", 2, 2))

db.session.commit()


