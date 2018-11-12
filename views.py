from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db,BookMessages,BookBadges,BookClass,user_favs,user_badges,user_cards,user_shares,Scroll,Users

admin = Admin(name='儿童绘本',template_mode='bootstrap3')

class BookMs(ModelView):
    column_list = ['book_id','class_id','title','title_cn','url']

class BookBd(ModelView):
    column_list = ['badges_id','url']

admin.add_view(BookMs(BookMessages,db.session,name='绘本信息'))
admin.add_view(BookBd(BookBadges,db.session,name='绘本图卡'))
admin.add_view(ModelView(BookClass,db.session,name='绘本分类',))
admin.add_view(ModelView(user_favs,db.session,name='用户收藏'))
admin.add_view(ModelView(user_badges,db.session,name='用户图卡'))
admin.add_view(ModelView(user_cards,db.session,name='用户卡券'))
admin.add_view(ModelView(user_shares,db.session,name='用户分享'))
admin.add_view(ModelView(Scroll,db.session,name='滚动条'))
admin.add_view(ModelView(Users,db.session,name='用户'))
