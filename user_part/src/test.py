#用来做一些闲杂测试，忽略即可

from werkzeug.security import generate_password_hash, check_password_hash
from Model import User, db 
from configs import IMAGEPATH
from uuid import uuid1 
import base64
import redis
import time
from Mail import send_email



print(len(str(uuid1())))