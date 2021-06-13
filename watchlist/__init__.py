import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')  # 等同于 app.secret_key = 'dev'

# 在扩展实例化前加载配置
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):   # 创建用户加载回调函数，接收user_id作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id))   # 用id作为User模型的主键查询对应的用户
    return user

login_manager.login_view = 'login'

@app.context_processor  # 注册一个模板上下文处理函数
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)  # 需返回字典，相当于return{'user':user}

from watchlist import views, errors, commands
