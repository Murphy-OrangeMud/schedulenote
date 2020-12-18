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
        #content_type = request.headers["Content-type"]

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
        #content_type = request.headers["Content-type"]

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
        #content_type = request.headers["Content-type"]

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
        # #content_type = request.headers["Content-type"]

        json = request.get_json()
        print(json)
        #json = request.json
        try:
            scheduleType = json["type"]
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
        except ValueError:
            return jsonify({"status": "information format incorrect"})
        except KeyError:
            return jsonify({"status": "information not complete"})
        except:
            return jsonify({"status": "schedule already added"})

@app.route("/deleteschedule", methods=("POST", ))
def deleteSchedule():
    if request.method == "POST":
        #content_type = request.headers["Content-type"]

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
        #content_type = request.headers["Content-type"]

        json = request.get_json()
        try:
            ID = json["id"]
        except KeyError:
            return jsonify({"status": "Fail: schedule id needed"})

        schedule = Schedule.query.filter_by(id=ID).first()
        if schedule == None:
            return jsonify({"status": "Fail: schedule does not exist"})
        
        try:
            scheduleType = json["type"]
        except KeyError:
            scheduleType = schedule.scheduleType

        try:
            description = json["description"]
        except KeyError:
            description = schedule.description

        try:
            location = json["location"]
        except KeyError:  
            location = schedule.location

        try:
            startTime = json["startTime"]
        except KeyError:
            startTime = "%04d-%02d-%02d %02d-%02d-%02d" % (schedule.startTime.year, 
                                                            schedule.startTime.month, 
                                                            schedule.startTime.day, 
                                                            schedule.startTime.hour, 
                                                            schedule.startTime.minute, 
                                                            schedule.startTime.second)
        
        try:
            endTime = json["endTime"]
        except KeyError:
            endTime = "%04d-%02d-%02d %02d-%02d-%02d" % (schedule.endTime.year, 
                                                        schedule.endTime.month, 
                                                        schedule.endTime.day, 
                                                        schedule.endTime.hour, 
                                                        schedule.endTime.minute, 
                                                        schedule.endTime.second)
        try:
            rotation = json["rotation"]
        except KeyError:
            rotation = schedule.rotation

        try:
            userID = json["userID"]
        except KeyError:
            userID = schedule.userID
        
        try:
            newschedule = Schedule(description, 
                                    location, 
                                    strformat2datetime(startTime), 
                                    strformat2datetime(endTime), 
                                    rotation, 
                                    userID, 
                                    scheduleType,
                                    ID)
        except:
            return jsonify({"status": "information format incorrect"})

        db.session.delete(schedule)
        db.session.add(newschedule)
        db.session.commit()

        return jsonify({"status": "OK", "schedule": {
                                                        "id": newschedule.id,
                                                        "userID": newschedule.userID,
                                                        "description": newschedule.description,
                                                        "location": newschedule.location,
                                                        "startTime": newschedule.startTime, 
                                                        "endTime": newschedule.endTime, 
                                                        "rotation": newschedule.rotation,
                                                        "type": newschedule.scheduleType
                                                    }})

# 规定：离ddl小于或等于24h的ddl被返回，待修改
@app.route("/getalert", methods=("POST", ))
def getAlert():
    if request.method == "POST":
        #content_type = request.headers["Content-type"]

        json = request.get_json()
        try:
            userID = json["userID"]
        except:
            return jsonify({"status": "Please provide userID"})

        current_time = datetime.datetime.now()
        
        alertList = Schedule.query.filter(Schedule.endTime > current_time).filter(Schedule.endTime <= current_time + datetime.timedelta(days=1)).filter_by(scheduleType=ScheduleTypes.DDL.value).filter_by(userID=userID).all()

        return_alert = []

        for schedule in alertList:
            return_alert.append({
                "id": schedule.id,
                "userID": schedule.userID,
                "description": schedule.description,
                "location": schedule.location,
                "startTime": schedule.startTime, 
                "endTime": schedule.endTime, 
                "rotation": schedule.rotation,
                "type": schedule.scheduleType
            })

        return jsonify({"status": "OK", "alertddl": return_alert})
    
@app.route("/save", methods=("GET", ))
def save():
    pass