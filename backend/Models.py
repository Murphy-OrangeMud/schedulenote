from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy 
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import uuid

from .configs import MAXSTRLEN, MAXMOTTO, MAXAVATAR, IMAGEPATH
from .utils import get_file_type
import redis

import datetime
from enum import Enum

db = SQLAlchemy(current_app)

class Note(db.Model):
    id = db.Column(db.String, primary_key=True, unique=True)
    sourceCode = db.Column(db.String)
    owner = db.Column(db.String)
    createTime = db.Column(db.DateTime, default=datetime.datetime.now)
    modifyTime = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    courseBelonged = db.Column(db.String)
    ups = db.Column(db.Integer, default=0)

    def __init__(self, source_code, owner, course_belonged):
        self.id = uuid.uuid1()
        self.sourceCode = source_code
        self.owner = owner
        self.courseBelonged = course_belonged

        
ScheduleTypes = Enum("ScheduleTypes", 
                    ("Class", 
                     "DDL",
                     "Exam"))

# sqlalchemy数据库中存Schedule对象，以id或者description作为主键
# 每个用户有一个calendar，因此calendar和user是一一映射关系。
# 想法：schedule增加id（随机生成的hash码）和userID两个属性
# 查询数据库时找到userID==指定userID的所有项然后按照起始时间排序
# syncWithPKU那个API放在User类当中（实现在下面）
class Schedule(db.Model):

    id = db.Column(db.String, primary_key=True, unique=True)
    description = db.Column(db.String(100), unique=False)  # 是否允许重复？
    location = db.Column(db.String(100))
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    rotation = db.Column(db.Integer)
    userID = db.Column(db.String(100))
    scheduleType = db.Column(db.Integer)

    """
        description (string): a description of the content of the schedule
        location (string): the location of the schedule
        startTime (datatime.time)
        endTime (datetime.datetime)
        rotation (int)
        userID (string): user who create this schedule
        scheduleType (int): 0 for class and 1 for ddl
    """
    def __init__(self, 
                 description, 
                 location, 
                 startTime, 
                 endTime, 
                 rotation,
                 userID,
                 scheduleType,
                 ID=None):
        self.description = description
        self.location = location
        self.startTime = startTime
        self.endTime = endTime
        self.rotation = rotation
        self.userID = userID
        self.scheduleType = scheduleType
        
        if ID == None:
            self.id = self.__generateID()
        else:
            self.id = ID

    def __repr__(self):
        startTime = "%04d-%02d-%02d %02d-%02d-%02d" % (self.startTime.year(), 
                                                       self.startTime.month(), 
                                                       self.startTime.day(), 
                                                       self.startTime.hour(), 
                                                       self.startTime.minute(), 
                                                       self.startTime.second())
        endTime = "%04d-%02d-%02d %02d-%02d-%02d" % (self.endTime.year(), 
                                                     self.endTime.month(), 
                                                     self.endTime.day(), 
                                                     self.endTime.hour(), 
                                                     self.endTime.minute(), 
                                                     self.endTime.second())
        return "<Schedule(description = '%s', location = '%s', startTime = '%s', endTime = '%s', rotation = '%d', userID = '%s', type = '%d'>" % (
            self.description, self.location, startTime, endTime, self.rotation, self.userID, self.type)

    def __generateID(self):
        import hashlib
        import json
        import time

        currentTime = time.strftime("%04d-%02d-%02d-%02d-%02d-%02d", time.localtime(time.time()))
        
        s = hashlib.sha1()
        s.update((self.startTime.strftime("%04d-%02d-%02d-%02d-%02d-%02d") + " " + 
                  self.endTime.strftime("%04d-%02d-%02d-%02d-%02d-%02d") + " " + 
                  self.userID + " " + 
                  str(self.scheduleType) + " " +
                  self.description).encode("utf-8"))
        return s.hexdigest()  

    def getSchedule(self):
        return self.ID

    def getScheduleDescription(self):
        return self.description

    def getLocation(self):
        return self.location

    def getStartTime(self):
        return self.startTime

    def getEndTime(self):
        return self.endTime

    def getRotation(self):
        return self.rotation

    def modifyScheduleDescription(self, newDescription):
        if isinstance(newDescription, str) and newDescription != None:
            self.description = newDescription

    def modifyLocation(self, newLocation):
        if isinstance(newLocation, str) and newLocation != None:
            self.location = newLocation

    def modifyStartTime(self, newStartTime):
        if isinstance(newStartTime, datetime.datetime) and newStartTime != None:
            self.startTime = newStartTime

    def modifyEndTime(self, newEndTime):
        if isinstance(newEndTime, datetime.datetime) and newEndTime != None:
            self.endTime = newEndTime

    def modifyRotation(self, newRotation):
        if isinstance(newRotation, int) and newRotation != None:
            self.rotation = newRotation      


class Calendar():
    def __init__(self, userID):
        self.userID = userID

    def showCalendar(self):
        calendar = Schedule.query.filter_by(userID=self.userID).order_by(Schedule.startTime)
        return calendar

    def addSchedule(self, schedule):
        db.session.add(schedule)
        db.session.commit()

    def deleteSchedule(self, schedule):
        db.session.delete(schedule)
        db.session.commit()

    # 如果没有哪一个参数，请指定为None。内部函数会检查参数。
    def modifySchedule(self, schedule, newDescription, newLocation, newStartTime, newEndTime, newRotation):
        schedule_m = Schedule.query.filter_by(ID=schedule.ID).first()
        schedule_m.modifyScheduleDescription(newDescription)
        schedule_m.modifyLocation(newLocation)
        schedule_m.modifyStartTime(newStartTime)
        schedule_m.modifyEndTime(newEndTime)
        schedule_m.modifyRotation(newRotation)
        db.session.delete(schedule)
        db.session.add(schedule_m)
        db.session.commit()

    def saveSchedule(self, schedule):
        pass

    def syncWithPKU(self, url):
        pass
    
    def sendAlert(self):
        pass



class File(db.Model):

    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    filename = db.Column(db.String(20))
    score = db.Column(db.Integer)
    uploader = db.Column(db.Integer)
    description = db.Column(db.Text)
    course = db.Column(db.Integer)

    def __init__(self, 
                 filename,
                 uploader,
                 description,
                 course):
        self.filename = filename
        self.uploader = uploader
        self.description = description
        self.course = course
        self.score = 0

    def save(self):
        db.session.add(self)
        db.session.commit()

    def upvote(self):
        self.score += 1
        db.session.commit()

    def downvote(self):
        self.score -= 1
        db.session.commit()


class Course(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    score = db.Column(db.Integer)
    info = db.Column(db.Text)

    def __init__(self,
                 id, 
                 name, 
                 info=""):

        self.id = id
        self.name = name
        self.info = info
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def addFile(self, newfile):
        file = File(newfile["filename"],newfile["uploader"],newfile["description"],self.id)
        file.save()

    def deleteFile(self, id):
        res = db.session.query(File).filter(File.id == id).delete()
        db.session.commit()
        return res

        
MyRedis = redis.Redis(host="localhost",port=6379,decode_responses=True)
#generate_password_hash得到的hash长度一定是93
PSW_HASH_LEN = 128

class User(UserMixin, db.Model):
    __tablename__ = "users_v1"

    id = db.Column(db.Integer,primary_key=True, nullable=False)
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
    
