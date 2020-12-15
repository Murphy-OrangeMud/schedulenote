import os
# 仅用作本地测试，待后端内容合并时统一修改
# Database Parameter
HOST = 'localhost'
PORT = '3306'
DATABASE = 'usertest'
USERNAME = 'root'
PASSWORD = ''


# Size Limits
MAXSTRLEN = 64 #username和password的最大值
MAXMOTTO = 64
MAXAVATAR = 64


# Path Configs
ROOTPATH = "D:/junior1/软件工程/项目开发/schedulenote/"
IMAGEPATH = ROOTPATH + "images/"

# App Configs
DB_URI = "mysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

SECRET_KEY = 'FOOLISH_KEY'