from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from User import User, db
from configs import MAXSTRLEN

user_bp = Blueprint('user', __name__)
login_manager = LoginManager()

def is_legal_str(s):
    if s:
        if len(s) > 0 and len(s) <= MAXSTRLEN:
            return True
    return False


@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id == userid).all()[0]


@user_bp.route('/login', methods = ['GET', 'POST'])
def login():
    name = request.values.get('name',type = str, default = None)
    password = request.values.get('password',type = str, default = None)
    user_data = {'code':0}

    if not current_user.is_anonymous:#当前有正在登录中的账号
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

@user_bp.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return_json = {}
    return_json['code'] = 200
    return_json['data'] = {}
    return_json['data']['msg'] = 'Logout Success'
    return jsonify(return_json)


@user_bp.route('/signup', methods = ['GET', 'POST'])
def signup():
    name = request.values.get('name',type = str, default = None)
    password = request.values.get('password',type = str, default = None)
    email = request.values.get('email',type = str, default = None)
    user_data = {
        'code' : 700, 
        'data' : {
            'msg':'parameter ILLEGAL', 
            'username':name, 
            'password': password, 
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
    #id和name只使用一个，不可同时使用，二者同时使用，id优先
    id = request.values.get('id', type = int, default = None)
    name = request.values.get('name', type = str, default = None)
    return_json = {'code': 400, 'data' : {}}
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
