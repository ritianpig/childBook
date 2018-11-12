from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class BookMessages(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    book_id = db.Column(db.String(30))
    class_id = db.Column(db.String(30))
    title = db.Column(db.String(100))
    title_cn = db.Column(db.String(100))
    url = db.Column(db.String(200))
    image = db.Column(db.String(200))
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
    book_id = db.Column(db.String(30))
    url = db.Column(db.String(200))
    badges = db.Column(db.Text)

class BookClass(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    class_id = db.Column(db.String(30))
    name = db.Column(db.String(100))

class Scroll(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    scroll = db.Column(db.Text)

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(200))
    isVip = db.Column(db.String(5),default='0')
    coins = db.Column(db.Integer,default=0)

# 用户收藏表
class user_favs(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(200))
    book_id = db.Column(db.String(30))

# 用户图卡表
class user_badges(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(200))
    book_id = db.Column(db.String(30))
    badge_id = db.Column(db.String(30))

# 用户卡券表
class user_cards(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(200))
    cards = db.Column(db.String(30))

class user_shares(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(200))
    book_id = db.Column(db.String(30))
    share_times = db.Column(db.Integer)

class Testa(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    test = db.Column(db.Text)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict