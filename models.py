from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class BookMessages(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    book_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    title_cn = db.Column(db.String(100))
    url = db.Column(db.String(200))
    cover = db.Column(db.String(200))
    mp3 = db.Column(db.String(200))
    time = db.Column(db.Integer)
    fav = db.Column(db.Integer)
    pages = db.Column(db.Text)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

class BookBadges(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    badges_id = db.Column(db.Integer)
    url = db.Column(db.String(200))
    badges = db.Column(db.Text)

class BookClass(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    class_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
