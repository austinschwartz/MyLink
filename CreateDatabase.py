from models import db, User, Picture, Album, Friend, Post

db.drop_all()
db.create_all()

# Users
db.session.add(User("George Foreman", "george@gmail.com", "abc123", "george.jpg"))
db.session.add(User("Mary Juana", "mary@gmail.com", "mary123", "mary.jpg"))
db.session.add(User("Peter", "peter@gmail.com", "peter134", "arms.jpg"))
db.session.add(User("Vanna Gentry", "ligula.Nullam.feugiat@Proinnon.ca", "hunter2", "kajsd.jpg"))
db.session.add(User("Amena Armstrong", "dictum@parturientmontes.net", "friedrice33", "mbnss.jpg"))
db.session.add(User("Tarik", "gobble@turkeys.org", "akj22", "notmary.jpg"))
db.session.add(User("Mary's Cousin", "juana@smoke.org", "drugsarebad", "alsonotmary.jpg"))

db.session.add(Friend(1, 2, "a"))
db.session.add(Friend(2, 1, "a"))

db.session.add(Friend(5, 1, "p"))
db.session.add(Friend(1, 5, "r"))

db.session.add(Friend(1, 3, "r")) # 1 is requesting 3 as friend
db.session.add(Friend(3, 1, "p")) # 3 has pending request from 1

db.session.add(Friend(1, 4, "d")) 
db.session.add(Friend(4, 1, "d"))

db.session.add(Album("album1", 1, "public"))
db.session.add(Album("album2", 1, "public"))
db.session.add(Album("album3", 1, "private"))
db.session.add(Album("album1", 2, "public"))
db.session.add(Album("Pictures of my dumb cat", 3, "public"))

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


