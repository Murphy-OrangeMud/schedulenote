from secret import *

# Size Limits
MAXSTRLEN = 64 #username和password的最大值
MAXMOTTO = 64
MAXAVATAR = 64
PSW_HASH_LEN = 128
MAXMSG = 200

# Path Configs
ROOTPATH = "/mnt/c/Users/cheng/schedulenote/"
IMAGEPATH = ROOTPATH + "images/"

#Redis Configs
REDIS_STAY_TIME = 300 #Redis中持续留存300s
REDISHOST = "localhost"
REDISPORT = 6379

# Mail Configs
MAIL_PORT = 465 #use SSL
MAIL_SERVER = "smtp.163.com"
MAIL_USEERNAME = 'schedulenote@163.com'
MAIL_PASSWORD = MAIL_PASSWORD
# App Configs
DB_URI = "mysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

SECRET_KEY = SECRET_KEY
