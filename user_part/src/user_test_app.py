# 用于测试User模块的功能
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash
import os

from configs import IMAGEPATH
from Model import db
from UserControler import user_bp, login_manager

app = Flask(__name__)
app.register_blueprint(user_bp,url_prefix='/user')
app.config.from_pyfile('configs.py')
app.app_context().push()
db.init_app(app)
login_manager.init_app(app)


if __name__ == "__main__":
    #在服务器上运行一次，就可以删掉了
    # if not os.path.exists(IMAGEPATH):
    #     os.makedirs(IMAGEPATH)
    db.create_all()
    app.run(debug=True)