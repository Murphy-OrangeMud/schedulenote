from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash
from configs import MAXSTRLEN, MAXMOTTO, MAXAVATER
db = SQLAlchemy()
#generate_password_hash得到的hash长度一定是93
PSW_HASH_LEN = 128

class User(UserMixin, db.Model):
    __tablename__ = "users_v1"

    id = db.Column(db.Integer,primary_key=True, nullable=False)
    username = db.Column(db.String(MAXSTRLEN), unique = True,  nullable=False)
    email = db.Column(db.String(MAXSTRLEN),  nullable=False)
    password= db.Column(db.String(PSW_HASH_LEN), nullable = False)
    avater = db.Column(db.String(MAXAVATER), nullable = True)
    motto = db.Column(db.String(MAXMOTTO), nullable = True)
    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.avater = None
        self.motto = None
    def __repr__(self):
        return '<User %r>' % self.username


    #以dict的形式返回user的全部信息（除了password）
    def todict(self):
        dic = {}
        dic['id'] = self.id
        dic['username'] = self.username
        dic['email'] = self.email
        dic['avater'] = self.avater
        dic['motto'] = self.motto
        return dic
    