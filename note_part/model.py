from flask import current_app
from flask_sqlalchemy import SQLAlchemy
import uuid
import datetime

db = SQLAlchemy(current_app)


class Note(db.Model):
    id = db.Column(db.String, primary_key=True, unique=True)
    sourceCode = db.Column(db.String)
    owner = db.Column(db.Integer)
    createTime = db.Column(db.DateTime, default=datetime.datetime.now)
    modifyTime = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    courseBelonged = db.Column(db.String)
    ups = db.Column(db.Integer, default=0)

    def __init__(self, source_code, owner, course_belonged):
        self.id = str(uuid.uuid1())
        self.sourceCode = source_code
        self.owner = owner
        self.courseBelonged = course_belonged


db.create_all()
