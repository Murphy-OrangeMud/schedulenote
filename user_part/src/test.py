#用来做一些闲杂测试，忽略即可

from werkzeug.security import generate_password_hash, check_password_hash
from User import User, db 
from configs import IMAGEPATH
from uuid import uuid1 
import base64
import redis
import time
import numpy as np
if __name__ == "__main__":
    r = redis.Redis(host="localhost",port=6379,decode_responses=True)
    r.set("1800013021@pku.edu.cn_checked", "1800013021@pku.edu.cn")



