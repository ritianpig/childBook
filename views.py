from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db,BookMessages,BookBadges,BookClass

admin = Admin(name='儿童绘本',template_mode='bootstrap3')

class BookMs(ModelView):
    column_list = ['book_id','class_id','title','title_cn','url','cover']

class BookBd(ModelView):
    column_list = ['badges_id','url']

admin.add_view(BookMs(BookMessages,db.session,name='绘本信息'))
admin.add_view(BookBd(BookBadges,db.session,name='绘本图卡'))
admin.add_view(ModelView(BookClass,db.session,name='绘本分类',))

