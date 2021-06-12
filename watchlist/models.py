from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db

class User(db.Model, UserMixin):  # 表名将会是user（自动生成，小写）
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):   # 用来设置密码的方法，接收密码作为参数
        self.password_hash = generate_password_hash(password)   # 将生成的密码保存到对应字段

    def validate_password(self, password):   # 用于验证密码的方法，接收密码作为参数
        return check_password_hash(self.password_hash, password)    # 返回布尔值


class Movies(db.Model):  # 表名是movies
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))