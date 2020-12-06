#仅用作本地测试，待后端内容合并时统一修改
HOST = 'localhost'
PORT = '3306'
DATABASE = 'usertest'
USERNAME = 'root'
PASSWORD = ''
MAXSTRLEN = 64

DB_URI = "mysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

SECRET_KEY = 'FOOLISH_KEY'