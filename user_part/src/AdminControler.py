from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from uuid import uuid1

from Model import User, db, MyRedis, Report, Feedback
from configs import *
from utils import get_file_type, is_legal_str, allowed_file, has_login, get_verify_code
from Mail import send_email

admin_bp = Blueprint('admin', __name__)

# 获得未完成的feedback的id
@admin_bp.route('/feedback_list', methods = ['GET'])
@login_required
def get_unfinished_feedback():
    return_json = {'data':{}} 
    if not current_user.is_admin():
        return_json['code'] = 400
        return_json['data']['msg'] = "You are not an administrator"
        return jsonify(return_json)
    unfin_list = Feedback.query.filter(Feedback.finished == 0)
    id_list = [fd.id for fd in unfin_list]
    return_json['code'] = 200
    return_json['data']['msg'] = "get unfinished feedback successfully"
    return_json['data']['id_list'] = id_list
    return jsonify(return_json)

@admin_bp.route('/report_list', methods = ['GET'])
@login_required
def get_unfinished_report():
    return_json = {'data':{}} 
    if not current_user.is_admin():
        return_json['code'] = 400
        return_json['data']['msg'] = "You are not an administrator"
        return jsonify(return_json)
    unfin_list = Report.query.filter(Report.finished == 0)
    id_list = [rp.id for rp in unfin_list]
    return_json['code'] = 200
    return_json['data']['msg'] = "get unfinished report successfully"
    return_json['data']['id_list'] = id_list
    return jsonify(return_json)


@admin_bp.route('/get_feedback/<id>', methods = ['GET'])
@login_required
def get_feedback(id):
    return_json = {'data':{}}
    if not current_user.is_admin(): 
        return_json['code'] = 400
        return_json['data']['msg'] = "You are not an administrator"
        return jsonify(return_json)
    try:
        return_json['data']["feedback"] = Feedback.query.get(id).todict()
        return_json['data']["msg"] = "feedback {id} get".format(id = id)
        return_json['code'] = 200
        return jsonify(return_json)
    except:
        return_json['data']["msg"] = "feedback {id} not exist".format(id = id)
        return_json['code'] = 300
        return jsonify(return_json)

@admin_bp.route('/get_report/<id>', methods = ['GET'])
@login_required
def get_report(id):
    return_json = {'data':{}}
    if not current_user.is_admin(): 
        return_json['code'] = 400
        return_json['data']['msg'] = "You are not an administrator"
        return jsonify(return_json)
    try:
        return_json['data']["report"] = Report.query.get(id).todict()
        return_json['data']["msg"] = "report {id} get".format(id = id)
        return_json['code'] = 200
        return jsonify(return_json)
    except:
        return_json['data']["msg"] = "report {id} not exist".format(id = id)
        return_json['code'] = 300
        return jsonify(return_json)

@admin_bp.route('/finish_feedback/<id>', methods = ['POST'])
@login_required
def finish_feedback(id):
    return_json = {'data':{}}
    if not current_user.is_admin(): 
        return_json['code'] = 400
        return_json['data']['msg'] = "You are not an administrator"
        return jsonify(return_json)
    try:
        this_feedback = Feedback.query.get(id)
        this_feedback.finished = 1
        db.session.commit()
        return_json['data']["msg"] = "feedback {id} finished".format(id = id)
        return_json['code'] = 200
        return jsonify(return_json)
    except:
        return_json['data']["msg"] = "feedback {id} not exist or database error".format(id = id)
        return_json['code'] = 300
        return jsonify(return_json)

@admin_bp.route('/finish_report/<id>', methods = ['POST'])
@login_required
def finish_report(id):
    return_json = {'data':{}}
    if not current_user.is_admin(): 
        return_json['code'] = 400
        return_json['data']['msg'] = "You are not an administrator"
        return jsonify(return_json)
    try:
        this_report = Report.query.get(id)
        this_report.finished = 1
        db.session.commit()
        return_json['data']["msg"] = "report {id} finished".format(id = id)
        return_json['code'] = 200
        return jsonify(return_json)
    except:
        return_json['data']["msg"] = "report {id} not exist or database error".format(id = id)
        return_json['code'] = 300
        return jsonify(return_json)

# UNFINISHED
# 删除文件部分还要和Note结合一下
@admin_bp.route('/admin_modify/<id>', methods = ['PUT'])
@login_required
def admin_modify(id):
    return_json = {'data':{}}
    #修改内容，0,1,2,3分别代表 昵称、头像、座右铭、笔记文件
    report_type = request.values.get('report_type', type = int, default = None)
    file_id = request.values.get('file_id', type = str, default = None)
    if not current_user.is_admin(): 
        return_json['code'] = 400
        return_json['data']['msg'] = "You are not an administrator"
        return jsonify(return_json)
    try:
        reported_user = User.query.get(id)
        # 改昵称
        if report_type == 0:
            reported_user.username = str(uuid1())
            db.session.commit()
            return_json['data']["msg"] = "Modify reported_user {name}'s {re_type} to \"{new_one}\" ".format(name = reported_user.name, re_type = "name", new_one = reported_user.username)
            return_json['code'] = 200
            return jsonify(return_json)
        elif report_type == 1:
            reported_user.avatar = None
            db.session.commit()
            return_json['data']["msg"] = "Modify reported_user {name}'s {re_type} to \"{new_one}\" ".format(name = reported_user.name, re_type = "avatar", new_one = "None")
            return_json['code'] = 200
            return jsonify(return_json)
        elif report_type == 2:
            reported_user.motto = None
            db.session.commit()
            return_json['data']["msg"] = "Modify reported_user {name}'s {re_type} to \"{new_one}\" ".format(name = reported_user.name, re_type = "motto", new_one = "None")
            return_json['code'] = 200
            return jsonify(return_json)
        elif report_type == 3:
            try:
                temp_note = Note.query.get(file_id)
                temp_note.sourceCode = None
                db.session.commit()
            except:
                return_json['data']["msg"] = "file id {id} error or database error".format(id = file_id)
                return_json['code'] = 300
                return jsonify(return_json)
        else:
            return_json['data']["msg"] = "Modify type undefined"
            return_json['code'] = 900
            return jsonify(return_json)
    except:
        return_json['data']["msg"] = "User {id} not exist or database error".format(id = id)
        return_json['code'] = 300
        return jsonify(return_json)

    