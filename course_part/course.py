import os
import json
from flask import Flask
from flask import jsonify,make_response
from flask import request,render_template,redirect,url_for,send_from_directory
from werkzeug.utils import secure_filename
from model import *
from pypinyin import lazy_pinyin
from pathlib import Path
app = Flask(__name__)
@app.route("/")
def index():
    return "hello"

@app.route("/course/filelist/",methods = ['GET'])
def queryList():
    if request.method == 'GET':
        session = Session()
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
        session.close()
        return jsonify(filelist)

@app.route("/course/upvote/",methods=['GET', 'POST'])
def upvote():
    if request.method == 'POST':
        session = Session()
        js = request.get_json()
        print(js)
        id = js["id"]
        file = session.query(File).filter(File.id == id).first()
        if file == None:
            return jsonify({"code":300}) # 找不到课程
        file.score += 1
        session.commit()
        session.close()        
        return jsonify({"code":200, "score" : file.score})
        

@app.route("/course/downvote/",methods=['GET', 'POST'])
def downvote():
    if request.method == 'POST':
        session = Session()
        js= request.get_json()
        id = js["id"]
        file = session.query(File).filter(File.id == id).first()      
        if file == None:
            return jsonify({"code":300}) # 找不到课程  
        file.score -= 1
        session.commit()
        session.close()
        return jsonify({"code":200 , "score" : file.score})
        

@app.route('/course/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # js = request.get_json()
        # print(js)
        session = Session()
        course = request.values.get("course",type=int,default = None)
        uploader = request.values.get("uploader",type=int,default = None)
        description = request.values.get("description",type=str,default = None)
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径\
        filename = secure_filename(''.join(lazy_pinyin(f.filename)))
        upload_path = os.path.join(basepath,Path(str(course)))
        isExists=os.path.exists(upload_path)
        if not isExists:
            os.makedirs(upload_path)
        upload_path = os.path.join(upload_path,filename)
        if os.path.isfile(upload_path):
            return jsonify({"code":400})
        f.save(upload_path)
        c = session.query(Course).filter(Course.id == course).first()
        c.addFile({"uploader":uploader,"description":description,"filename":f.filename})
        session.commit()
        session.close()
        return jsonify({"code":200})
    return jsonify({"code":0})

@app.route('/course/download/',methods=['GET','POST'])
def download():
    if request.method == "POST" or request.method == "GET":
        session = Session()
        id = request.values.get("id",type=int,default = None)
        print(id)
        file = session.query(File).filter(File.id == id).first()
        basepath = os.path.dirname(__file__)
        coursepath = Path(str(file.course))
        dfilename = secure_filename(''.join(lazy_pinyin(file.filename)))
        download_path = os.path.join(basepath,coursepath)
        session.close()        
        response = make_response(send_from_directory(download_path,filename=dfilename,as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(file.filename.encode().decode('latin-1'))
        return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000 ,debug=True)

    