from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from uuid import uuid1

from User import User, db
from configs import MAXSTRLEN, MAXMOTTO, MAXavatar, ROOTPATH, IMAGEPATH

user_bp = Blueprint('user', __name__)
login_manager = LoginManager()

def is_legal_str(s):
    if s:
        if len(s) > 0 and len(s) <= MAXSTRLEN:
            return True
    return False

#表示当前有正在登录的账号
def has_login():
    return not current_user.is_anonymous

@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id == userid).all()[0]


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
    #参数非法或用户不存在，均视为用户不存在
    user_data['code'] = 400
    user_data['data'] = {}
    user_data['data']['msg'] = 'User "' + name + '" doesn\'t exist'
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

# 修改个人信息, 包括username, motto, avatar，有原密码的password修改
# 暂时不包括 忘记password修改和email, 这两个需要邮件确认才可以
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
    
    newavatar = request.values.get('newavatar', type = str, default = None)
    # TODO

    #所有的都不满足，就一定是参数错误
    return_json['code'] = 900
    return_json['data']['msg'] = "parameter ILLEGAL"
    return jsonify(return_json)

@app.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    img = request.files.get('avatar')
    user_id = current_user.id
    filename = uuid1(user_id)
    path = IMAGEPATH
    file_path = path + filename
    img.save(file_path)
