from werkzeug.security import generate_password_hash, check_password_hash
from User import User, db 

user_data = {'code':0, 'data': {}}
name = 'hi'
user_data['data']['msg'] = 'hi"' + name + '"hi'

