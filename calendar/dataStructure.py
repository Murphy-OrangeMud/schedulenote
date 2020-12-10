import datetime
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
import data

db = SQLAlchemy(current_app)
db.create_all()

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
        self.description = description
        self.location = location
        self.startTime = startTime
        self.endTime = endTime
        self.rotation = rotation
        self.userID = userID
        self.type = scheduleType
        
        if ID == None:
            self.ID = self.__generateID()
        else:
            self.ID = ID

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

        currentTime = time.localtime(time.time())

        # 假定一个用户在一个时间戳范围内只能创建一个schedule（应该算合理假设）
        # 可以考虑修改（如何确保唯一性和排他性）
        s = hashlib.sha1()
        s.update(json.dumps(self.userID + " " + currentTime))
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
    """
        # Warning: 这个函数暂时用不了
        # TODO: 需要先处理登录
        # 从选课结果页面爬取课程数据的爬虫函数
        # url是选课结果页面的url，比如
        # https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/electiveWork/showResults.do

        import requests
        from bs4 import BeautifulSoup
        import re

        start_time_list = ["", 
                            datetime.datetime(hour=8), 
                            datetime.datetime(hour=9), 
                            datetime.datetime(hour=10, minute=10), 
                            datetime.datetime(hour=11, minute=10),
                            datetime.datetime(hour=13), 
                            datetime.datetime(hour=14), 
                            datetime.datetime(hour=15, minute=10), 
                            datetime.datetime(hour=16, minute=10), 
                            datetime.datetime(hour=17, minute=10), 
                            datetime.datetime(hour=18, minute=40), 
                            datetime.datetime(hour=19, minute=40), 
                            datetime.datetime(hour=20, minute=40)]

        end_time_list = ["", 
                        datetime.datetime(hour=8, minute=50), 
                        datetime.datetime(hour=9, minute=50), 
                        datetime.datetime(hour=11), 
                        datetime.datetime(hour=12), 
                        datetime.datetime(hour=13, minute=50), 
                        datetime.datetime(hour=14, minute=50), 
                        datetime.datetime(hour=16), 
                        datetime.datetime(hour=17), 
                        datetime.datetime(hour=18), 
                        datetime.datetime(hour=19, minute=30), 
                        datetime.datetime(hour=20, minute=30), 
                        datetime.datetime(hour=21, minute=30)]

        r = requests.get(url).text()
        
        if re.match(r, "出错提示"):
            return False
        
        r_m = r.replace("<br>", ",")
        bs = BeautifulSoup(r_m)
        class_list_even = bs.find_all(attrs = {"class": "course-even"})
        class_list_odd = bs.find_all(attrs = {"class": "course-odd"})

        def process_class_list(class_list, even=True):
            for i in range(class_list):
                class_col = class_list[i].find_all(attrs = {"class": "course"})

                for j in range(1, 8):
                    class_info = class_col[i].string
                    class_name = class_info[0]
                    class_location = class_info[1].strip('()')
                    class_rotation = class_info[2]
                    # 注意：要问一下rotation各个值的含义
                    rotation = -2

                    if re.match(class_rotation, "每周"):
                        rotation = -1
                    elif re.match(class_rotation, "双周"):
                        rotation = 0
                    else: #单周
                        rotation = 1

                    class_exam = class_info[3]

                    # 添加schedule，待修改：如何体现星期几
                    if (even):
                        new_class = Schedule(class_name, 
                                                class_location, 
                                                start_time_list[i*2+1], 
                                                end_time_list[i*2+1], 
                                                rotation, 
                                                self.userID, 
                                                ScheduleTypes.Class.value)
                    else:
                        new_class = Schedule(class_name, 
                                                class_location, 
                                                start_time_list[i*2+2], 
                                                end_time_list[i*2+2], 
                                                rotation, 
                                                self.userID, 
                                                ScheduleTypes.Class.value)

                    self.addSchedule(new_class)

                    # 是否要解析考试时间并添加schedule
                    start_time_exam_list = [datetime.datetime(hour=8, minute=30),
                                            datetime.datetime(hour=14),
                                            datetime.datetime(hour=18, minute=30)]
                    end_time_exam_list = [datetime.datetime(hour=10, minute=30), 
                                        datetime.datetime(hour=16), 
                                        datetime.datetime(hour=20, minute=30)]
                    
                    time_index = -1
                    
                    if re.match(class_exam, "上午"):
                        time_index = 0
                    elif re.match(class_exam, "下午"):
                        time_index = 1
                    else: # 晚上
                        time_index = 2
                    new_exam = Schedule(class_name + "期末考试", 
                                        None, 
                                        start_time_exam_list[time_index], 
                                        end_time_exam_list[time_index],
                                        -2,
                                        self.userID, 
                                        ScheduleTypes.Exam.value)

                    self.addSchedule(new_exam)

        process_class_list(class_list_even, True)
        process_class_list(class_list_odd, False)
    """

    def sendAlert(self):
        pass