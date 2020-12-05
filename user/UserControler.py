from flask import Blueprint, request, make_response, jsonify
from User import User, db
from werkzeug.security import generate_password_hash, check_password_hash
import json
from configs import MAXSTRLEN

user_bp = Blueprint('user', __name__)

def is_legal_str(s):
    if s:
        if len(s) > 0 and len(s) <= MAXSTRLEN:
            return True
    return False

@user_bp.route('/login', methods = ['POST'])
def login():
    pass

@user_bp.route('/logout')
def logout():
    pass

@user_bp.route('/signup', methods = ['POST'])
def signup():
    name = request.values.get('name')
    password = request.values.get('password')
    email = request.values.get('email')
    user_data = {'code' : 700, 'data' : {'msg':'parameter ILLEGAL', 'username':name, 'password': password, 'email': email} }
    if is_legal_str(name) and is_legal_str(password) and is_legal_str(email):
        if User.query.filter(User.username == name).all():
            user_data['code'] = 400
            user_data['data']['msg'] = 'User ' + name + ' already exits'
            return jsonify(user_data)
        try:
            user = User(name, password, email)
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            user_data['code'] = 200
            user_data['data']['msg'] = 'Signup Success'
            return jsonify(user_data)
        except:
            user_data['code'] = 300
            user_data['data']['msg'] = 'Database error'
            return jsonify(user_data)
    else:
        return jsonify(user_data)

