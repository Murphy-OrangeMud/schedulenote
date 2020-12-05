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
    name = request.values.get('name')
    password = request.values.get('password')
    user_data = {'code':0}
    if is_legal_str(name) and is_legal_str(password):
        #判断用户是否存在
        user_search = User.query.filter(User.username == name).all()
        if user_search:
            user = user_search[0]
            if check_password_hash(user.password, password):
                print("look here1", current_user)
                login_user(user)
                print("look here2",current_user)
                user_data['code'] = 200
                user_data['data'] = user.todict()
                user_data['data']['msg'] = 'User "' + name + '" login success'
                return jsonify(user_data)
            else: #密码错误
                user_data['code'] = 400
                user_data['data'] = {}
                user_data['data']['msg'] = 'Password to '' User "' + name + '" is error'
                return jsonify(user_data)
        else:#用户不存在
            user_data['code'] = 400
            user_data['data'] = {}
            user_data['data']['msg'] = 'User "' + name + '" doesn\'t exist'
            return jsonify(user_data)
    else:#参数非法
        user_data['code'] = 700
        user_data['data'] = {
            'msg':'parameter ILLEGAL', 
            'username':name, 
            'password': password,
        }
        return jsonify(user_data)

@user_bp.route('/logout')
@login_required
def logout():
    print(current_user)
    logout_user()
    return_json = {}
    return_json['code'] = 200
    return_json['data'] = {}
    return_json['data']['msg'] = 'Logout Success'
    return jsonify(return_json)


@user_bp.route('/signup', methods = ['GET', 'POST'])
def signup():
    name = request.values.get('name')
    password = request.values.get('password')
    email = request.values.get('email')
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

