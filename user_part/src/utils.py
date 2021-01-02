from configs import MAXSTRLEN
# from flask_login import current_user
from uuid import uuid1
from flask import session

def is_legal_str(s):
    try:
        if s:
            if len(s) > 0 and len(s) <= MAXSTRLEN:
                return True
    except:
        pass
    return False

#表示当前有正在登录的账号
def has_login():
    return session.get('user_id')


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'JPEG', 'JPG', 'PNG']
 
def get_file_type(filename):
    if is_legal_str(filename):
        try:
            return filename.rsplit('.', 1)[1]
        except:
            pass
    return None

def allowed_file(filename):
    return '.' in filename and  get_file_type(filename) in ALLOWED_EXTENSIONS

def get_verify_code():
    return str(uuid1())[:6]
