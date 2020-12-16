from configs import MAXSTRLEN
from flask_login import current_user


def is_legal_str(s):
    if s:
        if len(s) > 0 and len(s) <= MAXSTRLEN:
            return True
    return False

#表示当前有正在登录的账号
def has_login():
    return not current_user.is_anonymous


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'JPEG', 'JPG', 'PNG']
 
def get_file_type(filename):
    return filename.rsplit('.', 1)[1]

def allowed_file(filename):
    return '.' in filename and  get_file_type(filename) in ALLOWED_EXTENSIONS