from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from uuid import uuid1

from Model import User, db, MyRedis, Report, Feedback
from configs import *
from utils import get_file_type, is_legal_str, allowed_file, has_login, get_verify_code
from Mail import send_email

user_bp = Blueprint('user', __name__)
login_manager = LoginManager()

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





@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

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
    return_json = {'data':{}}
    email = request.values.get('email',type = str, default = None)
    if not is_legal_str(email):
        return_json['code'] = 900
        return_json['data']['msg'] = "Email can't use or Network congestion"
        return jsonify(return_json)
    if MyRedis.get(email) != None:
        verify_code = MyRedis.get(email)
    else:
        verify_code = get_verify_code()
        MyRedis.set(email, verify_code, REDIS_STAY_TIME)
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
    user_data = {'code':0, 'data':{}}

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
                # print(user.todict())
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
        user = User.query.get(id)
        if user:
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

#################反馈相关###########################
# 反馈意见
# msg为反馈内容
# anonymous取0或1，表示用户是否选择匿名
@user_bp.route('/feedback', methods = ['POST'])
@login_required
def feedback():
    msg = request.values.get('msg', type = str, default = None)
    anonymous = request.values.get('anonymous', type = int, default = None)
    return_json = {'code' : 900,'data':{}}
    if msg == None:
        return_json['data']['msg'] = "message can not be None or Too long(over 200 bytes)"
        return jsonify(return_json)
    elif len(msg) == 0 or len(msg) > MAXMSG:
        return_json['data']['msg'] = "message can not be None or Too long(over 200 bytes)"
        return jsonify(return_json)
    else: #msg合法
        my_feedback = Feedback(msg)
        if anonymous == 0:
            my_feedback = Feedback(msg, current_user.id)
        try:
            db.session.add(my_feedback)
            db.session.flush()
            db.session.commit()
        except:
            return_json['code'] = 300
            return_json['data']['msg'] = 'Database error'
            return jsonify(return_json)
        return_json['code'] = 200
        return_json['data']['msg'] = "feedback success"
        return jsonify(return_json)

@user_bp.route('/report', methods = ['POST'])
@login_required
def report():
    msg = request.values.get('msg', type = str, default = None)
    #被举报者id
    reported_id = request.values.get('reported_id', type = int, default = None)
    #举报内容，0,1,2,3分别代表 昵称、头像、座右铭、笔记文件
    to_report = request.values.get('to_report', type = int, default = None)
    #文件号，如果to_report=3则必填
    file_id = request.values.get('file_id', type = str, default = None)
    #是否匿名，取0 or 1
    anonymous = request.values.get('anonymous', type = int, default = None)
    return_json = {'code' : 900,'data':{}}
    #被举报者不存在
    if not User.query.get(reported_id):
        return_json['code'] = 400
        return_json['data']['msg'] = "User does not exists"
        return jsonify(return_json)
    #举报内容为文件，文件号为空
    if to_report == 3 and file_id == None:
        return_json['code'] = 900
        return_json['data']['msg'] = "Error: file_id empty"
        return jsonify(return_json)
    # msg非法
    if msg == None:
        return_json['data']['msg'] = "message can not be None or Too long(over 200 bytes)"
        return jsonify(return_json)
    elif len(msg) == 0 or len(msg) > MAXMSG:
        return_json['data']['msg'] = "message can not be None or Too long(over 200 bytes)"
        return jsonify(return_json)

    else: #msg合法
        my_id = current_user.id
        if anonymous == 0:
            my_id = -1
        my_report = Report(reported_id, to_report, msg, file_id, my_id)
        try:
            db.session.add(my_report)
            db.session.flush()
            db.session.commit()
        except:
            return_json['code'] = 300
            return_json['data']['msg'] = 'Database error'
            return jsonify(return_json)
        return_json['code'] = 200
        return_json['data']['msg'] = "report success"
        return jsonify(return_json)
