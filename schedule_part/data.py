from flask import request
from flask import jsonify
from flask import current_app
from flask import render_template
from flask import Blueprint
import datetime

from dataStructure import ScheduleTypes
from dataStructure import Schedule
from dataStructure import db

app = Blueprint("schedule", __name__, url_prefix='/schedule')

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
        userID = json["userID"]

        print(userID)

        calendar = Schedule.query.filter_by(userID=userID).order_by(Schedule.startTime)

        return_calendar = []
        for schedule in calendar:
            return_calendar.append({
                "id": schedule.id,
                "userID": schedule.userID,
                "description": schedule.description,
                "location": schedule.location,
                "startTime": schedule.startTime, 
                "endTime": schedule.endTime, 
                "rotation": schedule.rotation,
                "type": schedule.scheduleType
            })

        return jsonify({"status": "OK", "calendar": return_calendar})

@app.route("/getclasscalendar", methods=("POST",))
def getClassCalendar():
    if request.method == "POST":
        content_type = request.headers["Content-type"]

        json = request.get_json()
        userID = json["userID"]

        calendar = Schedule.query.filter_by(userID=userID, scheduleType=ScheduleTypes.Class.value).order_by(Schedule.startTime)

        return_calendar = []
        for schedule in calendar:
            return_calendar.append({
                "id": schedule.id,
                "userID": schedule.userID,
                "description": schedule.description,
                "location": schedule.location,
                "startTime": schedule.startTime, 
                "endTime": schedule.endTime, 
                "rotation": schedule.rotation,
                "type": schedule.scheduleType
            })

        return jsonify({"status": "OK", "calendar": return_calendar})

@app.route("/getdeadlinescalendar", methods=("POST", ))
def getDeadlinesCalendar():
    if request.method == "POST":
        content_type = request.headers["Content-type"]

        json = request.get_json()
        userID = json["userID"]

        calendar = Schedule.query.filter_by(userID=userID, scheduleType=ScheduleTypes.DDL.value).order_by(Schedule.endTime)

        return_calendar = []
        for schedule in calendar:
            return_calendar.append({
                "id": schedule.id,
                "userID": schedule.userID,
                "description": schedule.description,
                "location": schedule.location,
                "startTime": schedule.startTime, 
                "endTime": schedule.endTime, 
                "rotation": schedule.rotation,
                "type": schedule.scheduleType
            })

        return jsonify({"status": "OK", "calendar": return_calendar})

@app.route("/updateclassschedule", methods=("GET", ))
def updateClassSchedule():
    pass 

@app.route("/addschedule", methods=("POST", ))
def addSchedule():
    if request.method == "POST":
        # content_type = request.headers["Content-type"]

        json = request.get_json()
        print(json)
        #json = request.json
        
        scheduleType = json["type"]

        # 修改：是不是直接改成addSchedule而不要检查type，直接dispatch
        # if scheduleType != ScheduleTypes.DDL.value:
        #    return jsonify({"status": "Fail: not a ddl"})

        description = json["description"]
        location = json["location"]
        startTime = json["startTime"]
        endTime = json["endTime"]
        rotation = json["rotation"]
        userID = json["userID"]
        
        newschedule = Schedule(description, 
                          location, 
                          strformat2datetime(startTime), 
                          strformat2datetime(endTime), 
                          rotation, 
                          userID, 
                          scheduleType)

        db.session.add(newschedule)
        db.session.commit()

        return jsonify({"status": "OK"})

@app.route("/deleteschedule", methods=("POST", ))
def deleteSchedule():
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
        
@app.route("/modifyschedule", methods=("POST", ))
def modifySchedule():
    if request.method == "POST":
        content_type = request.headers["Content-type"]

        json = request.get_json()

        ID = json["id"]
        schedule = Schedule.query.filter_by(id=ID).first()
        if schedule == None:
            return jsonify({"status": "Fail: schedule does not exist"})
        
        scheduleType = json["type"]
        # if scheduleType != ScheduleTypes.DDL.value:
        #     return jsonify({"status": "Fail: not a ddl"})

        description = json["description"]
        if description == "":  # 或约定一个值代表这一项不需要修改，下同
            description = schedule.description

        location = json["location"]
        if location == "":  
            location = schedule.location

        startTime = json["startTime"]
        if startTime == "":
            startTime = "%04d-%02d-%02d %02d-%02d-%02d" % (schedule.startTime.year(), 
                                                            schedule.startTime.month(), 
                                                            schedule.startTime.day(), 
                                                            schedule.startTime.hour(), 
                                                            schedule.startTime.minute(), 
                                                            schedule.startTime.second())
        endTime = json["endTime"]
        if endTime == "":
            endTime = "%04d-%02d-%02d %02d-%02d-%02d" % (schedule.endTime.year(), 
                                                        schedule.endTime.month(), 
                                                        schedule.endTime.day(), 
                                                        schedule.endTime.hour(), 
                                                        schedule.endTime.minute(), 
                                                        schedule.endTime.second())
        rotation = json["rotation"]
        if rotation <= -10:
            rotation = schedule.rotation

        userID = json["userID"]
        if userID == "":
            userID = schedule.userID
        
        newschedule = Schedule(description, 
                          location, 
                          strformat2datetime(startTime), 
                          strformat2datetime(endTime), 
                          rotation, 
                          userID, 
                          scheduleType,
                          ID)

        db.session.delete(schedule)
        db.session.add(newschedule)
        db.session.commit()

        return jsonify({"status": "OK"})

# 规定：离ddl小于或等于24h的ddl被返回，待修改
@app.route("/getalert", methods=("GET", ))
def getAlert():
    if request.method == "GET":
        current_time = datetime.datetime.now()
        
        alertList = Schedule.query.filter(Schedule.startTime <= current_time + datetime.timedelta(days=1)).filter_by(scheduleType=ScheduleTypes.DDL.value).all()

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
    pass