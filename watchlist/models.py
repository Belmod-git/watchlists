from watchlist import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from sqlalchemy import Column,Integer,String
import datetime

class User(db.Model,UserMixin):
    id = Column(Integer,primary_key=True) # 主键
    name = Column(String(20))
    username = Column(String(20))   # 用户名
    password_hash = Column(String(128)) #密码散列值

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)


class Ariticles(db.Model):
    id = Column(Integer,primary_key=True) # 主键
    title = Column(String(60))
    content = Column(String(1000))
    author = Column(String(20))
    pubdate = Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
