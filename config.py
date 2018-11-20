import os

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:129426@127.0.0.1:3306/childBook?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
JSON_AS_ASCII = False
SCHEDULER_API_ENABLED = True