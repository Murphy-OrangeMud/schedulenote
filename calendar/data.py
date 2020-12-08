from flask import request
from flask import jsonify
from flask import current_app
from flask import render_template
from flask import Blueprint
import datetime

from dataStructure import ScheduleTypes
from dataStructure import Schedule
from dataStructure import db

app = Blueprint("data", __name__)

def strformat2datetime(strformat):
    year = strformat[0:4]
    month = strformat[5:7]
    day = strformat[8:10]
    hour = strformat[11:13]
    minute = strformat[14:16]
    second = strformat[17:19]

    return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

@app.route("/getcalendar", methods=("POST", ))
def getCalendar():
    if request.method == "POST":
        content_type = request.headers["Content-type"]

        json = request.get_json()
        userID = json["userID"][0]

        # to be revised: 按照起始时间排序还是终止时间？
        calendar = Schedule.query.filter_by(userID=userID).order_by(Schedule.startTime)

        return_calendar = []
        for schedule in calendar:
            return_calendar.append({
                "id": schedule.ID,
                "userID": schedule.userID,
                "description": schedule.description,
                "location": schedule.location,
                "startTime": schedule.startTime, 
                "endTime": schedule.endTime, 
                "rotation": schedule.rotation,
                "type": schedule.type
            })

        return jsonify({"status": "OK", "calendar": return_calendar})

@app.route("/getclasscalendar", methods=("POST",))
def getClassCalendar():
    if request.method == "POST":
        content_type = request.headers["Content-type"]

        json = request.get_json()
        userID = json["userID"][0]

        calendar = Schedule.query.filter_by(userID=userID, scheduleType=ScheduleTypes.Class.value).order_by(Schedule.startTime)

        return_calendar = []
        for schedule in calendar:
            return_calendar.append({
                "id": schedule.ID,
                "userID": schedule.userID,
                "description": schedule.description,
                "location": schedule.location,
                "startTime": schedule.startTime, 
                "endTime": schedule.endTime, 
                "rotation": schedule.rotation,
                "type": schedule.type
            })

        return jsonify({"status": "OK", "calendar": return_calendar})

@app.route("/getdeadlinescalendar", methods=("POST", ))
def getDeadlinesCalendar():
    if request.method == "POST":
        content_type = request.headers["Content-type"]

        json = request.get_json()
        userID = json["userID"][0]

        # to be revised: DDL按照起始时间排序还是终止时间？
        calendar = Schedule.query.filter_by(userID=userID, scheduleType=ScheduleTypes.DDL.value).order_by(Schedule.startTime)

        return_calendar = []
        for schedule in calendar:
            return_calendar.append({
                "id": schedule.ID,
                "userID": schedule.userID,
                "description": schedule.description,
                "location": schedule.location,
                "startTime": schedule.startTime, 
                "endTime": schedule.endTime, 
                "rotation": schedule.rotation,
                "type": schedule.type
            })

        return jsonify({"status": "OK", "calendar": return_calendar})

@app.route("/updateclassschedule", methods=("GET", ))
def updateClassSchedule():
    pass # TODO: 如何刷新页面？还是说似乎也不需要这个操作……

@app.route("/addddl", methods=("POST", ))
def addDDL():
    if request.method == "POST":
        content_type = request.headers["Content-type"]

        json = request.get_json()
        
        scheduleType = json["type"]
        
        # 修改：是不是直接改成addSchedule而不要检查type，直接dispatch
        if scheduleType != ScheduleTypes.DDL.value:
            return jsonify({"status": "Fail: not a ddl"})

        description = json["description"]
        location = json["location"]
        startTime = json["startTime"]
        endTime = json["endTime"]
        rotation = json["rotation"]
        userID = json["userID"]
        
        newDDL = Schedule(description, 
                          location, 
                          strformat2datetime(startTime), 
                          strformat2datetime(endTime), 
                          rotation, 
                          userID, 
                          ScheduleTypes.DDL.value)

        db.session.add(newDDL)
        db.session.commit()

        return jsonify({"status": "OK"})

@app.route("/deleteddl", methods=("POST", ))
def deleteDDL():
    if request.method == "POST":
        content_type = request.headers["Content-type"]

        json = request.get_json()
        ID = json["id"]
        schedule = Schedule.query.filter_by(id=ID).first()

        if schedule == None:
            return jsonify({"status": "Fail: Schedule does not exist"})

        db.session.delete(schedule)
        db.session.commit()

        return jsonify({"status": "OK"})
        
@app.route("/modifyddl", methods=("POST", ))
def modifyDDL():
    if request.method == "POST":
        content_type = request.headers["Content-type"]

        json = request.get_json()

        ID = json["id"]
        DDL = Schedule.query.filter_by(id=ID).first()
        if DDL == None:
            return jsonify({"status": "Fail: ddl does not exist"})
        
        scheduleType = json["type"]
        if scheduleType != ScheduleTypes.DDL.value:
            return jsonify({"status": "Fail: not a ddl"})

        description = json["description"]
        if description == None:  # 或约定一个值代表这一项不需要修改，下同
            description = DDL.description

        location = json["location"]
        if location == None:  
            location = DDL.location

        startTime = json["startTime"]
        if startTime == None:
            startTime = "%04d-%02d-%02d %02d-%02d-%02d" % (DDL.startTime.year(), 
                                                            DDL.startTime.month(), 
                                                            DDL.startTime.day(), 
                                                            DDL.startTime.hour(), 
                                                            DDL.startTime.minute(), 
                                                            DDL.startTime.second())
        endTime = json["endTime"]
        if endTime == None:
            endTime = "%04d-%02d-%02d %02d-%02d-%02d" % (DDL.endTime.year(), 
                                                        DDL.endTime.month(), 
                                                        DDL.endTime.day(), 
                                                        DDL.endTime.hour(), 
                                                        DDL.endTime.minute(), 
                                                        DDL.endTime.second())
        rotation = json["rotation"]
        if rotation == None:
            rotation = DDL.rotation

        userID = json["userID"]
        if userID == None:
            userID = DDL.userID
        
        newDDL = Schedule(description, 
                          location, 
                          strformat2datetime(startTime), 
                          strformat2datetime(endTime), 
                          rotation, 
                          userID, 
                          ScheduleTypes.DDL.value,
                          ID)

        db.session.delete(DDL)
        db.session.add(newDDL)
        db.session.commit()

        return jsonify({"status": "OK"})

# 规定：离ddl小于或等于24h的ddl被返回，待修改
@app.route("/getalert", methods=("GET", ))
def getAlert():
    if request.method == "GET":
        current_time = datetime.datetime.now()
        
        alertList = Schedule.query.filter_by(Schedule.startTime <= current_time + datetime.timedelta(days=1), 
                                            type=ScheduleTypes.DDL.value).all()

        return_alert = []

        for schedule in alertList:
            return_alert.append({
                "id": schedule.ID,
                "userID": schedule.userID,
                "description": schedule.description,
                "location": schedule.location,
                "startTime": schedule.startTime, 
                "endTime": schedule.endTime, 
                "rotation": schedule.rotation,
                "type": schedule.type
            })

        return jsonify({"status": "OK", "alertddl": return_alert})
    
@app.route("/save", methods=("GET", ))
def save():
    pass  # TODO: 似乎目前的API会自动保存，不需要这个操作……