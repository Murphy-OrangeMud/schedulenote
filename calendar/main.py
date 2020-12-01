# 临时文件，用于生成和测试日历部分。后续需要合并

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# to be revised
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'