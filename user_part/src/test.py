#用来做一些闲杂测试，忽略即可

from werkzeug.security import generate_password_hash, check_password_hash
from User import User, db 
from configs import IMAGEPATH
from uuid import uuid1 
import base64
 
avatarpath = IMAGEPATH + "49e0875c-3ecb-11eb-8b78-000000000004.jpeg"
img_stream = None
with open(avatarpath, 'rb') as img_f:
    img_stream = base64.b64encode(img_f.read()) 

