import datetime
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy(current_app)

ScheduleTypes = Enum("ScheduleTypes", 
                    ("Class", 
                     "DDL"))

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
    userID = db.Column(db.String(100), unique=True)
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
        if ID == None:
            self.ID = self.__generateID()
        else:
            self.ID = ID

        self.description = description
        self.location = location
        self.startTime = startTime
        self.endTime = endTime
        self.rotation = rotation
        self.userID = userID
        self.type = scheduleType

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
        # TODO: generate SHA-1 value
        return 0  

    # 感觉这些成员函数都不需要。。
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

    # TODO: 思考还需要如何考虑corner case检验这些新值的合法性
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

def syncWithPKU():
    pass  # TODO: 写爬虫从选课网爬取数据，需要和用户管理耦合/交互

"""
# to be revised: 直接使用数据库处理列表，不用calendar这玩意    
class Calendar():
    # user: to be revised
    def __init__(self, userID):
        self.scheduleList = []
        self.userID = userID

    def showCalendar(self):
        pass

    def addSchedule(self, schedule):
        self.scheduleList.append(schedule)

    def deleteSchedule(self, schedule):
        self.scheduleList.remove(schedule)

    # 如果没有哪一个参数，请指定为None。内部函数会检查参数。
    def modifySchedule(self, schedule, newDescription, newLocation, newStartTime, newEndTime, newRotation):
        schedule.modifyScheduleDescription(newDescription)
        schedule.modifyStartTime(newStartTime)
        schedule.modifyEndTime(newEndTime)
        schedule.modifyLocation(newLocation)
        schedule.modifyRotation(newRotation)

    def saveSchedule(self, schedule):
        pass

    def syncWithPKU(self):
        pass

    def sendAlert(self):
        pass
"""