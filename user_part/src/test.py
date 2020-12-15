#用来做一些闲杂测试，忽略即可

from werkzeug.security import generate_password_hash, check_password_hash
from User import User, db 
from uuid import uuid1 

print(len(str(uuid1())))

