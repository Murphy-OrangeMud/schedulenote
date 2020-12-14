import os
import json
from flask import Flask
from flask import jsonify
from flask import request,render_template,redirect,url_for
from werkzeug.utils import secure_filename
from model import *

app = Flask(__name__)
@app.route("/")
def index():
    return "hello"

@app.route("/course/filelist/",methods = ['GET'])
def queryList():
    if request.method == 'GET':
        files = session.query(File).all()
        filelist = []
        for file in files:
            uploader = file.uploader
            course = session.query(Course).filter(Course.id == file.course).first()
            coursename = course.name
            score = file.score
            filename = file.filename
            fileid = file.id
            filedict = {"uploader" : uploader,
                        "coursename": coursename,
                        "score": score,
                        "filename": filename,
                        "fileid": fileid,
                        "courseid":course.id
                        }
            filelist.append(filedict)
        return jsonify(filelist)

@app.route("/course/upvote/",methods=['GET', 'POST'])
def upvote():
    if request.method == 'POST':
        # request.
        js = request.get_json()
        print(js)
        id = js["id"]
        file = session.query(File).filter(File.id == id).first()
        file.score += 1
        session.commit()
        return jsonify({"code":200, "score" : file.score})
        

@app.route("/course/downvote/",methods=['GET', 'POST'])
def downvote():
    if request.method == 'POST':
        js= request.get_json()
        id = js["id"]
        file = session.query(File).filter(File.id == id).first()
        file.score -= 1
        session.commit()
        return jsonify({"code":200 , "score" : file.score})
        

@app.route('/course/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath,secure_filename(f.filename))
        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('upload.html')

# from note_part.data import *
# from schedule_part.data import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

    