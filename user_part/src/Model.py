from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash
import base64

from configs import *
from utils import get_file_type
import redis
db = SQLAlchemy()
MyRedis = redis.Redis(host=REDISHOST,port=REDISPORT,decode_responses=True)


class User(UserMixin, db.Model):
    __tablename__ = "users_v3"

    id = db.Column(db.Integer,primary_key=True, nullable=False)
    isAdmin = db.Column(db.Integer, nullable = False)
    username = db.Column(db.String(MAXSTRLEN), unique = True,  nullable=False)
    email = db.Column(db.String(MAXSTRLEN),  unique = True, nullable=False)
    password= db.Column(db.String(PSW_HASH_LEN), nullable = False)
    avatar = db.Column(db.String(MAXAVATAR), nullable = True)
    motto = db.Column(db.String(MAXMOTTO), nullable = True)
    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.avatar = None
        self.motto = None
        self.isAdmin = 0
    def __repr__(self):
        return '<User %r>' % self.username

    def is_admin(self):
        return self.isAdmin != 0

    #以dict的形式返回user的全部信息（除了password）
    def todict(self):
        dic = {}
        dic['id'] = self.id
        dic['username'] = self.username
        dic['email'] = self.email
        dic['is_admin'] = self.isAdmin
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


to_report_type = ["username", "avatar", "motto", "note"]
class Report(db.Model):
    __tablename__ = "report"
    id = db.Column(db.Integer,primary_key=True, nullable=False)
    finished = db.Column(db.Integer, nullable = False)
    reported_id = db.Column(db.Integer, nullable=False) #被举报者
    #被举报类型，包括昵称、头像、座右铭、笔记文件四种，分别用0、1、2、3代表
    to_report = db.Column(db.Integer, nullable=False) 
    msg = db.Column(db.String(MAXMSG), nullable = False)
    file_id = db.Column(db.String(MAXSTRLEN), nullable=True) #这里与Note部分对接，他使用的str(uuid1)作为id
    whistleBlower_id = db.Column(db.Integer, nullable=True) #举报者，可以为空
    def __init__(self, reported, to_report, msg, file_id = None, whistleBlower = -1):
        self.reported_id = reported
        self.to_report = to_report
        self.msg = msg
        self.file_id = file_id
        self.whistleBlower_id = whistleBlower
        self.finished = 0

    def todict(self):
        dic = {}
        dic['id'] = self.id
        dic['finished'] = self.finished
        dic['reported_id'] = self.reported_id
        dic['to_report'] = to_report_type[self.to_report]
        dic['msg'] = self.msg
        dic['file_id'] = self.file_id
        dic['whistleBlower_id'] = self.whistleBlower_id
        return dic

class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer,primary_key=True, nullable=False)
    finished = db.Column(db.Integer, nullable = False)
    msg = db.Column(db.String(MAXMSG), nullable = False)
    whistleBlower_id = db.Column(db.Integer, nullable=True) #提意见的用户
    
    def __init__(self, msg, whistleBlower = -1):
        self.msg = msg
        self.whistleBlower_id = whistleBlower
        self.finished = 0

    def todict(self):
        dic = {}
        dic['id'] = self.id
        dic['finished'] = self.finished
        dic['msg'] = self.msg
        dic['whistleBlower_id'] = self.whistleBlower_id
        return dic
