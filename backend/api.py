import os
import json
import functools
from flask import render_template, redirect, url_for, send_from_directory, make_response, session
from werkzeug.utils import secure_filename

from .Models import *

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from uuid import uuid1

from pypinyin import lazy_pinyin
from pathlib import Path
from .configs import *

from .utils import get_file_type, is_legal_str, allowed_file, has_login, get_verify_code
from .utils import send_email
from .utils import strformat2datetime, datetime2strformat

import markdown, pdfkit


course_bp = Blueprint("course", __name__, url_prefix='/course')
note_bp = Blueprint("note", __name__, url_prefix='/note')
schedule_bp = Blueprint("schedule", __name__, url_prefix='/schedule')
user_bp = Blueprint('user', __name__, url_prefix='/user')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
#login_manager = LoginManager()

@course_bp.route("/courselist", methods=['GET'])
def courseList():
    if request.method == 'GET':
        courses = db.session.query(Course).all()
        courselist = []
        for course in courses:
            id = course.id
            name = course.name
            info = course.info
            coursedict = {"id": id,
                        "name": name,
                        "info": info,
                        }
            courselist.append(coursedict)
        return jsonify(courselist)

@course_bp.route("/queryFile", methods=['GET','POST'])
def queryFile():
    if request.method == 'GET' or request.method == 'POST':
        id = request.values.get("id",type=int,default = None)
        if id == None:
            return jsonify({"code":10})
        files = db.session.query(File).filter(File.course == id).all()
        filelist = []
        for file in files:
            uploader = file.uploader
            course = db.session.query(Course).filter(Course.id == file.course).first()
            coursename = course.name
            score = file.score
            filename = file.filename
            fileid = file.id
            filedict = {"uploader": uploader,
                        "coursename": coursename,
                        "score": score,
                        "filename": filename,
                        "fileid": fileid,
                        "courseid": course.id
                        }
            filelist.append(filedict)
        return jsonify(filelist)


@course_bp.route("/filelist", methods=['GET'])
def queryList():
    if request.method == 'GET':
        files = db.session.query(File).all()
        filelist = []
        for file in files:
            uploader = file.uploader
            course = db.session.query(Course).filter(Course.id == file.course).first()
            if course == None:
                continue
            coursename = course.name
            score = file.score
            filename = file.filename
            fileid = file.id
            filedict = {"uploader": uploader,
                        "coursename": coursename,
                        "score": score,
                        "filename": filename,
                        "fileid": fileid,
                        "courseid": course.id
                        }
            filelist.append(filedict)
        return jsonify(filelist)


@course_bp.route("/upvote", methods=['GET', 'POST'])
def upvote():
    if request.method == 'POST':
        # request.
        js = request.get_json()
        print(js)
        id = js["id"]
        file = db.session.query(File).filter(File.id == id).first()
        file.score += 1
        db.session.commit()
        return jsonify({"code": 200, "score": file.score})


@course_bp.route("/downvote", methods=['GET', 'POST'])
def downvote():
    if request.method == 'POST':
        js = request.get_json()
        id = js["id"]
        file = db.session.query(File).filter(File.id == id).first()
        file.score -= 1
        db.session.commit()
        return jsonify({"code": 200, "score": file.score})


@course_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        session = db.session
        course = request.values.get("course",type=int,default = None)
        uploader = request.values.get("uploader",type=int,default = None)
        description = request.values.get("description",type=str,default = None)
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径\
        filename = secure_filename(''.join(lazy_pinyin(f.filename)))
        upload_path = os.path.join(basepath,Path(str(course)))
        isExists=os.path.exists(upload_path)
        if not isExists:
            os.makedirs(upload_path)
        upload_path = os.path.join(upload_path,filename)
        if os.path.isfile(upload_path):
            return jsonify({"code":400})
        f.save(upload_path)
        c = session.query(Course).filter(Course.id == course).first()
        c.addFile({"uploader":uploader,"description":description,"filename":f.filename})
        session.commit()
        return jsonify({"code":200})
    return jsonify({"code":0})

@course_bp.route('/download',methods=['GET','POST'])
def download():
    if request.method == "POST" or request.method == "GET":
        session = db.session
        id = request.values.get("id",type=int,default = None)
        print(id)
        file = session.query(File).filter(File.id == id).first()
        basepath = os.path.dirname(os.path.abspath(__file__))
        coursepath = Path(str(file.course))
        dfilename = secure_filename(''.join(lazy_pinyin(file.filename)))
        download_path = os.path.join(basepath,coursepath)
        print(download_path)
        print(dfilename)
        session.commit()    
        response = make_response(send_from_directory(download_path,filename=dfilename,as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(file.filename.encode().decode('latin-1'))
        return response
@course_bp.route('/deleteCourse',methods=['GET','POST'])
def deleteCourse():
    id = request.values.get("id",type=int,default = None)
    if id == None:
        return jsonify({"code":0})
    course = Course.query.get(id)
    if course == None:
        return jsonify({"code":0})
    session = db.session
    session.delete(course)
    session.commit()
    session.close()
    return jsonify({"code":200})
@course_bp.route('/addCourse',methods=['GET','POST'])
def addCourse():
    name = request.values.get("name",type=str,default = None)
    info = request.values.get("info",type=str,default = "")
    print(name,info)
    if name == None:
        return jsonify({"code":0})
    course = Course(name,info)
    course.save()
    return jsonify({"code":200})

@note_bp.route("/modifyNotes", methods=["POST"])
def modityNotes():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        newSourceCode = json["sourceCode"]
        note = Note.query.get(ID)
        if note is None:  # 试图修改不存在的笔记
            return jsonify({"status": "ERR"})
        note.sourceCode = newSourceCode
        db.session.commit()
        return jsonify({"status": "OK"})

@note_bp.route("/exportPDF", methods=["POST"])
def exportPDF():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        path = 'pdfGenerated/'
        fileName = ID + '.pdf'
        note = Note.query.get(ID)
        if note==None:
            return jsonify({"status": "ERR"})
        pdfkit.from_string(markdown.markdown(note.sourceCode), "test")
        return make_response(send_from_directory(os.path.join(note_bp.root_path, path), fileName, as_attachment=True))


@note_bp.route("/newNote", methods=["POST"])
def newNote():
    if request.method == "POST":
        json = request.get_json()
        newNote = Note(json["sourceCode"], json["owner"], json["course_belonged"])
        db.session.add(newNote)
        db.session.commit()
        return jsonify({"status": "OK"})


@note_bp.route("/upVote", methods=["POST"])
def upVote():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        note = Note.query.get(ID)
        if note==None:
            return jsonify({"status": "ERR"})
        note.ups += 1
        db.session.commit()
        return jsonify({"status": "OK"})


@note_bp.route("/downVote", methods=["POST"])
def downVote():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        note = Note.query.get(ID)
        if note==None:
            return jsonify({"status": "ERR"})
        note.ups -= 1
        db.session.commit()
        return jsonify({"status": "OK"})


@note_bp.route("/getNote", methods=["POST"])
def getNote():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        note = Note.query.get(ID)
        if note==None:
            return jsonify({"status": "ERR"})
        return jsonify(
            {"sourceCode": note.sourceCode, "owner": note.owner, "createTime": note.createTime,
             "modifyTime": note.modifyTime, "courseBelonged": note.courseBelonged, "ups": note.ups})


@note_bp.route("/getAllNoteID", methods=["GET"])
def getAllNoteID():
    if request.method == "GET":
        IDList = []
        for note in Note.query.all():
            IDList.append(note.id)
        return jsonify(IDList)


@note_bp.route("/previewNote", methods=["POST"])
def previewNote():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        note = Note.query.get(ID)
        if note is None:  # 试图预览不存在的笔记
            return jsonify({"status": "ERR"})
        return jsonify(markdown.Markdown(note.sourceCode))


@schedule_bp.route("/getcalendar", methods=("POST",))
def getCalendar():
    if request.method == "POST":
        # content_type = request.headers["Content-type"]

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
                "startTime": datetime2strformat(schedule.startTime),
                "endTime": datetime2strformat(schedule.endTime),
                "rotation": schedule.rotation,
                "type": schedule.scheduleType
            })

        return jsonify({"status": "OK", "calendar": return_calendar})


@schedule_bp.route("/getclasscalendar", methods=("POST",))
def getClassCalendar():
    if request.method == "POST":
        # content_type = request.headers["Content-type"]

        json = request.get_json()
        userID = json["userID"]

        calendar = Schedule.query.filter_by(userID=userID, scheduleType=ScheduleTypes.Class.value).order_by(
            Schedule.startTime)

        return_calendar = []
        for schedule in calendar:
            return_calendar.append({
                "id": schedule.id,
                "userID": schedule.userID,
                "description": schedule.description,
                "location": schedule.location,
                "startTime": datetime2strformat(schedule.startTime),
                "endTime": datetime2strformat(schedule.endTime),
                "rotation": schedule.rotation,
                "type": schedule.scheduleType
            })

        return jsonify({"status": "OK", "calendar": return_calendar})


@schedule_bp.route("/getdeadlinescalendar", methods=("POST",))
def getDeadlinesCalendar():
    if request.method == "POST":
        # content_type = request.headers["Content-type"]

        json = request.get_json()
        userID = json["userID"]

        calendar = Schedule.query.filter_by(userID=userID, scheduleType=ScheduleTypes.DDL.value).order_by(
            Schedule.endTime)

        return_calendar = []
        for schedule in calendar:
            return_calendar.append({
                "id": schedule.id,
                "userID": schedule.userID,
                "description": schedule.description,
                "location": schedule.location,
                "startTime": datetime2strformat(schedule.startTime),
                "endTime": datetime2strformat(schedule.endTime),
                "rotation": schedule.rotation,
                "type": schedule.scheduleType
            })

        return jsonify({"status": "OK", "calendar": return_calendar})


@schedule_bp.route("/updateclassschedule", methods=("GET",))
def updateClassSchedule():
    pass


@schedule_bp.route("/addschedule", methods=("POST",))
def addSchedule():
    if request.method == "POST":
        # #content_type = request.headers["Content-type"]

        json = request.get_json()
        print(json)
        # json = request.json
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


@schedule_bp.route("/deleteschedule", methods=("POST",))
def deleteSchedule():
    if request.method == "POST":
        # content_type = request.headers["Content-type"]

        json = request.get_json()
        ID = json["id"]
        schedule = Schedule.query.filter_by(id=ID).first()

        if schedule == None:
            return jsonify({"status": "Fail: Schedule does not exist"})

        db.session.delete(schedule)
        db.session.commit()

        return jsonify({"status": "OK"})


@schedule_bp.route("/modifyschedule", methods=("POST",))
def modifySchedule():
    if request.method == "POST":
        # content_type = request.headers["Content-type"]

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
            "startTime": datetime2strformat(newschedule.startTime),
            "endTime": datetime2strformat(newschedule.endTime),
            "rotation": newschedule.rotation,
            "type": newschedule.scheduleType
        }})


# 规定：离ddl小于或等于24h的ddl被返回，待修改
@schedule_bp.route("/getalert", methods=("POST",))
def getAlert():
    if request.method == "POST":
        # content_type = request.headers["Content-type"]

        json = request.get_json()
        try:
            userID = json["userID"]
        except:
            return jsonify({"status": "Please provide userID"})

        current_time = datetime.datetime.now()

        alertList = Schedule.query.filter(Schedule.endTime > current_time).filter(
            Schedule.endTime <= current_time + datetime.timedelta(days=1)).filter_by(
            scheduleType=ScheduleTypes.DDL.value).filter_by(userID=userID).all()

        return_alert = []

        for schedule in alertList:
            return_alert.append({
                "id": schedule.id,
                "userID": schedule.userID,
                "description": schedule.description,
                "location": schedule.location,
                "startTime": datetime2strformat(schedule.startTime),
                "endTime": datetime2strformat(schedule.endTime),
                "rotation": schedule.rotation,
                "type": schedule.scheduleType
            })

        return jsonify({"status": "OK", "alertddl": return_alert})


@schedule_bp.route("/save", methods=("GET",))
def save():
    pass


# APIs

@user_bp.route('/test_init', methods = ['GET', 'POST'])
def test_init():
    user1 = User('alice', '123', 'alice@email')
    user2 = User('admin', '123', 'admin@email')
    db.session.add(user1)
    db.session.flush()
    db.session.commit()
    user2.isAdmin = 1
    db.session.add(user2)
    db.session.flush()
    db.session.commit()
    feed1 = Feedback("msg1")
    db.session.add(feed1)
    db.session.flush()
    db.session.commit()
    feed2 = Feedback("msg2")
    db.session.add(user2)
    db.session.flush()
    db.session.commit()
    rep1 = Report(1, 1, "msg1")
    db.session.add(feed1)
    db.session.flush()
    db.session.commit()
    rep2 = Report(1, 1, "msg2")
    db.session.add(rep2)
    db.session.flush()
    db.session.commit()
    return "success"


@user_bp.route('/login', methods = ['POST'])
def login():
    name = request.values.get('name',type = str, default = None)
    password = request.values.get('password',type = str, default = None)
    user_data = {'code':0, 'data':{}}
    if is_legal_str(name) and is_legal_str(password):
        #判断用户是否存在
        user_search = User.query.filter(User.username == name).all()
        if user_search:
            user = user_search[0]
            if check_password_hash(user.password, password):
                user_data['code'] = 200
                user_data['data'] = user.todict()
                user_data['data']['msg'] = 'User "' + name + '" login success'
                return jsonify(user_data)
            else: #密码错误
                user_data['code'] = 400
                user_data['data'] = {}
                user_data['data']['msg'] = 'Password to '' User "' + name + '" is error'
                return jsonify(user_data)
        else:
            #用户不存在
            user_data['code'] = 400
            user_data['data'] = {}
            user_data['data']['msg'] = 'User "' + name + '" doesn\'t exist'
            return jsonify(user_data)
    #参数非法
    user_data['code'] = 900
    user_data['data'] = {}
    user_data['data']['msg'] = 'parameter ILLEGAL'
    return jsonify(user_data)         

@user_bp.route('/logout', methods = ['POST'])
def logout():
    return_json = {}
    return_json['code'] = 200
    return_json['data'] = {}
    return_json['data']['msg'] = 'Logout Success'
    return jsonify(return_json)


@user_bp.route('/signup', methods = ['POST'])
def signup():
    name = request.values.get('name',type = str, default = None)
    password = request.values.get('password',type = str, default = None)
    email = request.values.get('email',type = str, default = None)
    user_data = {
        'code' : 700, 
        'data' : {
            'msg':'parameter ILLEGAL', 
            'username':name, 
            'email': email
        } 
    }
    if is_legal_str(name) and is_legal_str(password) and is_legal_str(email):
        if User.query.filter(User.username == name).all():
            user_data['code'] = 400
            user_data['data']['msg'] = 'User "' + name + '" already exists'
            return jsonify(user_data)
        if User.query.filter(User.email == email).all():
            user_data['code'] = 400
            user_data['data']['msg'] = 'The mailbox is already occupied'
            return jsonify(user_data)
        user = User(name, password, email)
        try:
            db.session.add(user)
            db.session.flush()
            db.session.commit()
        except:
            user_data['code'] = 300
            user_data['data']['msg'] = 'Database error'
            return jsonify(user_data)
        user_data['code'] = 200
        user_data['data']['id'] = user.id
        user_data['data']['msg'] = 'Signup Success'
        return jsonify(user_data)
    else:
        return jsonify(user_data)

@user_bp.route("/getuser", methods = ['GET'])
def get_user():
    name = request.values.get('name', type = str, default = None)
    return_json = {'code': 400, 'data' : {}}
    if id != None:
        user = User.query.get(id)
        if user:
            return_json['code'] = 200
            return_json['data'] = user.todict()
            return_json['data']['msg'] = 'success'
            return jsonify(return_json)
    if is_legal_str(name):
        userlist = User.query.filter(User.username == name).all()
        if userlist:
            user = userlist[0]
            return_json['code'] = 200
            return_json['data'] = user.todict()
            return_json['data']['msg'] = 'success'
            return jsonify(return_json)
    return_json['data']['msg'] = "user can't be visited or parameter ILLEGAL"
    return jsonify(return_json)

# 修改个人信息, 包括username, motto 有原密码的password修改, email
# 头像涉及到文件，所以单独写了upload_avatar接口
@user_bp.route("/modify", methods = ['PUT'])
def modify_info():
    return_json = {'data':{}}
    name = request.values.get('name', type = str, default = None)
    try:
        current_user = User.query.filter(User.username == name)[0]
    except:
        return_json['code'] = 400
        return_json['data']['msg'] = "username error"
        return jsonify(return_json)
    
    newname = request.values.get('newname', type = str, default = None)
    if is_legal_str(newname):
        if User.query.filter(User.username == newname).all():
            return_json['code'] = 400
            return_json['data']['msg'] = "User \"" + newname  + "\" already exists"
            return jsonify(return_json)
        else:
            current_user.username = newname
            db.session.commit()
            return_json['code'] = 200
            return_json['data']['msg'] = "Username modify success"
            return jsonify(return_json)

    newpassword = request.values.get('newpassword', type = str, default = None)
    if is_legal_str(newpassword):
        current_user.password = generate_password_hash(newpassword)
        db.session.commit()
        return_json['code'] = 200
        return_json['data']['msg'] = "Password modify success"
        return jsonify(return_json)

    newmotto = request.values.get('newmotto', type = str, default = None)
    if newmotto:
        if len(newmotto) > 0 and len(newmotto) <= MAXMOTTO:
            current_user.motto = newmotto
            db.session.commit()
            return_json['code'] = 200
            return_json['data']['msg'] = "Motto modify success"
            return jsonify(return_json)

    newemail = request.values.get('newemail', type = str, default = None)
    if is_legal_str(newemail):
        try:
            current_user.email = newemail
            db.session.commit()
            return_json['code'] = 200
            return_json['data']['msg'] = "Email modify success"
            return jsonify(return_json)
        except:
            return_json['code'] = 900
            return_json['data']['msg'] = "The mailbox is already occupied"
            return jsonify(return_json)
        
    #所有的都不满足，就一定是参数错误
    return_json['code'] = 900
    return_json['data']['msg'] = "parameter ILLEGAL"
    return jsonify(return_json)



# 上传用户头像
@user_bp.route('/upload_avatar', methods=['PUT'])
def upload_avatar():
    return_json = {'data':{}}
    name = request.values.get('name', type = str, default = None)
    try:
        current_user = User.query.filter(User.username == name)[0]
    except:
        return_json['code'] = 400
        return_json['data']['msg'] = "username error"
        return jsonify(return_json)
    img = request.files.get('avatar')
    user_id = current_user.id
    if allowed_file(img.filename):
        ext = get_file_type(img.filename)
        filename = str(uuid1(user_id)) + '.' + ext
        path = IMAGEPATH
        file_path = path + filename
        current_user.avatar = filename
        db.session.commit()
        img.save(file_path)
        return_json['code'] = 200
        return_json['data']['msg'] = 'success'
        return jsonify(return_json)
    return_json['code'] = 900
    return_json['data']['msg'] = 'abnormal image type'
    return jsonify(return_json)

