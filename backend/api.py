import os
import json
from flask import render_template, redirect,url_for, send_from_directory, make_response
from werkzeug.utils import secure_filename

from Models import *

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from uuid import uuid1

from configs import *

from utils import get_file_type, is_legal_str, allowed_file, has_login, get_verify_code
from utils import send_email

import markdown, pdfkit

course_bp = Blueprint("course", __name__, url_prefix='/course')
note_bp = Blueprint("note", __name__, url_prefix='/note')
schedule_bp = Blueprint("schedule", __name__, url_prefix='/schedule')
user_bp = Blueprint('user', __name__, url_prefix='/user')
login_manager = LoginManager()

@course_bp.route("/filelist",methods = ['GET'])
def queryList():
    if request.method == 'GET':
        files = db.session.query(File).all()
        filelist = []
        for file in files:
            uploader = file.uploader
            course = db.session.query(Course).filter(Course.id == file.course).first()
            coursename = course.name
            score = file.score
            filename = file.filename
            fileid = file.id
            filedict = {"uploader" : uploader,
                        "coursename": coursename,
                        "score": score,
                        "filename": filename,
                        "fileid": fileid,
                        "courseid":course.id
                        }
            filelist.append(filedict)
        return jsonify(filelist)

@course_bp.route("/upvote",methods=['GET', 'POST'])
def upvote():
    if request.method == 'POST':
        # request.
        js = request.get_json()
        print(js)
        id = js["id"]
        file = db.session.query(File).filter(File.id == id).first()
        file.score += 1
        db.session.commit()
        return jsonify({"code":200, "score" : file.score})
        

@course_bp.route("/downvote",methods=['GET', 'POST'])
def downvote():
    if request.method == 'POST':
        js= request.get_json()
        id = js["id"]
        file = db.session.query(File).filter(File.id == id).first()
        file.score -= 1
        db.session.commit()
        return jsonify({"code":200 , "score" : file.score})
        

@course_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath,secure_filename(f.filename))
        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('upload.html')


@note_bp.route("/modifyNotes", methods=["POST"])
def modityNotes():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        newSourceCode = json["sourceCode"]
        note = Note.query.get(ID)
        note.sourceCode = newSourceCode
        db.session.commit()
        return jsonify({"status": "OK"})


@note_bp.route("/previewNote", methods=["POST"])
def previewNote():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        return jsonify(markdown.Markdown(Note.query.get(ID).sourceCode))


@schedule_bp.route("/getcalendar", methods=("POST", ))
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

@schedule_bp.route("/getclasscalendar", methods=("POST",))
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

@schedule_bp.route("/getdeadlinescalendar", methods=("POST", ))
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

@schedule_bp.route("/updateclassschedule", methods=("GET", ))
def updateClassSchedule():
    pass 

@schedule_bp.route("/addschedule", methods=("POST", ))
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

@schedule_bp.route("/deleteschedule", methods=("POST", ))
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
        
@schedule_bp.route("/modifyschedule", methods=("POST", ))
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
@schedule_bp.route("/getalert", methods=("POST", ))
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
    
@schedule_bp.route("/save", methods=("GET", ))
def save():
    pass



# APIs
@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id == userid).all()[0]

@user_bp.route('/search_email', methods = ['GET'])
def search_email():
    email = request.values.get('email',type = str, default = None)
    return_json = {"data":{}}
    if User.query.filter(User.email == email).all():
        return_json['code'] = 200
        return_json['data']['msg'] = 'success'
        return jsonify(return_json)
    else:
        return_json['code'] = 400
        return_json['data']['msg'] = 'User not exist'
        return jsonify(return_json)


# 先获取验证码
# 在signup, login_by_mail, modify mail的时候，需要检查<email_checked, email>是否在Redis中
@user_bp.route('/get_mail_verify', methods = ['GET'])
def get_mail_verify():
    email = request.values.get('email',type = str, default = None)
    if MyRedis.get(email) != None:
        verify_code = MyRedis.get(email)
    else:
        verify_code = get_verify_code()
        MyRedis.set(email, verify_code, REDIS_STAY_TIME)
    return_json = {'data':{}}
    if send_email(email, verify_code) == -1:
        #发送失败，可能是网络问题或者email有误
        return_json['code'] = 900
        return_json['data']['msg'] = "Email can't use or Network congestion"
        return jsonify(return_json)
    else:
        return_json['code'] = 200
        return_json['data']['msg'] = "Get verify code successfully"
        return jsonify(return_json)

# 确认验证码，验证成功后，将<email_checked, email>存到MyRedis中，持续时长为REDIS_STAY_TIME = 300s
@user_bp.route('/check_mail_verify', methods = ['POST'])
def check_mail_verify():
    email = request.values.get('email',type = str, default = None)
    verify_code = request.values.get('verify_code',type = str, default = None)
    return_json = {'data':{}}
    if verify_code == MyRedis.get(email):
        MyRedis.set(email+"_checked", email, REDIS_STAY_TIME) #把email本身存在Redis里，确认后赋予权限
        MyRedis.delete(email)
        return_json['code'] = 200
        return_json['data']['msg'] = "Check verify code successfully"
        return jsonify(return_json)
    else:
        if MyRedis.get(email) != None:
            return_json['code'] = 900
            return_json['data']['msg'] = "Verify code error"
            return jsonify(return_json)
        else:
            return_json['code'] = 900
            return_json['data']['msg'] = "The verification code does not exist or has expired"
            return jsonify(return_json)
        

@user_bp.route('/login', methods = ['POST'])
def login():
    name = request.values.get('name',type = str, default = None)
    password = request.values.get('password',type = str, default = None)
    user_data = {'code':0}

    if has_login():#当前有正在登录中的账号
        user_data['code'] = 400
        user_data['data'] = {}
        user_data['data']['msg'] = 'User "' + current_user.username + '" is using now'
        return jsonify(user_data)
    if is_legal_str(name) and is_legal_str(password):
        #判断用户是否存在
        user_search = User.query.filter(User.username == name).all()
        if user_search:
            user = user_search[0]
            if check_password_hash(user.password, password):
                login_user(user)
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

@user_bp.route('/login_by_email', methods = ['POST'])
def login_by_email():
    user_data = {'data':{}}
    email = request.values.get('email',type = str, default = None)
    if MyRedis.get(email+'_checked') == email:
        MyRedis.delete(email + '_checked')
        user_search = User.query.filter(User.email == email).all()
        if user_search:
            user = user_search[0]
            login_user(user)
            user_data['code'] = 200
            user_data['data'] = user.todict()
            user_data['data']['msg'] = 'User "' + user.username + '" login success'
            return jsonify(user_data)
        else:
            user_data['code'] = 400
            user_data['data']['msg'] = 'User doesn\'t exist'
            return jsonify(user_data)
    else:
        user_data['code'] = 400
        user_data['data']['msg'] = 'The mailbox was not verified'
        return jsonify(user_data)
         

@user_bp.route('/logout', methods = ['POST'])
@login_required
def logout():
    logout_user()
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
        if MyRedis.get(email + '_checked') != email:
            user_data['code'] = 400
            user_data['data']['msg'] = 'The mailbox was not verified'
            return jsonify(user_data)
        MyRedis.delete(email + '_checked')
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
    #id和name二者都空则查看自己的信息，二者都非空则以id为准
    id = request.values.get('id', type = int, default = None)
    name = request.values.get('name', type = str, default = None)
    return_json = {'code': 400, 'data' : {}}
    if id == None and name == None:
        if has_login():
            return_json['code'] = 200
            return_json['data'] = current_user.todict()
            return_json['data']['msg'] = 'success'
            return_json['data']['is_current'] = 1
            return jsonify(return_json)
    if id != None:
        userlist = User.query.filter(User.id == id).all()
        if userlist:
            user = userlist[0]
            return_json['code'] = 200
            return_json['data'] = user.todict()
            return_json['data']['msg'] = 'success'
            try:
                return_json['data']['is_current'] = int(current_user == user)
            except:
                return_json['data']['is_current'] = 0
            return jsonify(return_json)
    if is_legal_str(name):
        userlist = User.query.filter(User.username == name).all()
        if userlist:
            user = userlist[0]
            return_json['code'] = 200
            return_json['data'] = user.todict()
            return_json['data']['msg'] = 'success'
            try:
                return_json['data']['is_current'] = int(current_user == user)
            except:
                return_json['data']['is_current'] = 0
            return jsonify(return_json)
    return_json['data']['msg'] = "user can't be visited or parameter ILLEGAL"
    return jsonify(return_json)

# 修改个人信息, 包括username, motto 有原密码的password修改
# email修改需要先完成邮件验证
# 头像涉及到文件，所以单独写了upload_avatar接口
@user_bp.route("/modify", methods = ['PUT'])
@login_required
def modify_info():
    return_json = {'data':{}}
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
        if MyRedis.get(newemail + "_checked") == newemail:
            current_user.motto = newmotto
            db.session.commit()
            return_json['code'] = 200
            return_json['data']['msg'] = "Email modify success"
            return jsonify(return_json)
        else:
            return_json['code'] = 400
            return_json['data']['msg'] = 'The mailbox was not verified'
            return jsonify(return_json)
    #所有的都不满足，就一定是参数错误
    return_json['code'] = 900
    return_json['data']['msg'] = "parameter ILLEGAL"
    return jsonify(return_json)



# 上传用户头像
@user_bp.route('/upload_avatar', methods=['PUT'])
@login_required
def upload_avatar():
    img = request.files.get('avatar')
    return_json = {'data':{}}
    user_id = current_user.id
    if allowed_file(img.filename):
        ext = get_file_type(img.filename)
        filename = str(uuid1(user_id)) + '.' + ext
        path = IMAGEPATH
        file_path = path + filename
        current_user.avatar = filename
        db.session.commit()
        # print(current_user.avatar)
        img.save(file_path)
        return_json['code'] = 200
        return_json['data']['msg'] = 'success'
        return jsonify(return_json)
    return_json['code'] = 900
    return_json['data']['msg'] = 'abnormal image type'
    return jsonify(return_json)

login_manager.init_app(current_app)