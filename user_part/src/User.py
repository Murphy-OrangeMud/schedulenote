from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash
import base64

from configs import MAXSTRLEN, MAXMOTTO, MAXAVATAR, IMAGEPATH
from utils import get_file_type
db = SQLAlchemy()
#generate_password_hash得到的hash长度一定是93
PSW_HASH_LEN = 128

class User(UserMixin, db.Model):
    __tablename__ = "users_v1"

    id = db.Column(db.Integer,primary_key=True, nullable=False)
    username = db.Column(db.String(MAXSTRLEN), unique = True,  nullable=False)
    email = db.Column(db.String(MAXSTRLEN),  nullable=False)
    password= db.Column(db.String(PSW_HASH_LEN), nullable = False)
    avatar = db.Column(db.String(MAXAVATAR), nullable = True)
    motto = db.Column(db.String(MAXMOTTO), nullable = True)
    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.avatar = None
        self.motto = None
    def __repr__(self):
        return '<User %r>' % self.username


    #以dict的形式返回user的全部信息（除了password）
    def todict(self):
        dic = {}
        dic['id'] = self.id
        dic['username'] = self.username
        dic['email'] = self.email
        #将文件编程base64图片流传给前端
        dic['avatar'] = {}
        if self.avatar == None:
            dic['avatar']['code'] = 400
        else:
            avatarpath = IMAGEPATH + self.avatar
            print(avatarpath)
            try:
                with open(avatarpath, 'rb') as img_f:
                    img_stream = base64.b64encode(img_f.read()) 
                    dic['avatar'] = {}
                    dic['avatar']['code'] = 200
                    dic['avatar']['img_type'] = get_file_type(self.avatar)
                    dic['avatar']['img_stream'] = img_stream
            except:
                dic['avatar']['code'] = 300
        dic['motto'] = self.motto
        return dic
    