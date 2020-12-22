#用来做一些闲杂测试，忽略即可

from werkzeug.security import generate_password_hash, check_password_hash
from User import User, db 
from configs import IMAGEPATH
from uuid import uuid1 
import base64
import redis
import time
import numpy as np
from Mail import send_email
if __name__ == "__main__":
    send_email("1800013021@pku.edu.cn", 123456)



