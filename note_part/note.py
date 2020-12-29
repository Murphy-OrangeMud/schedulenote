from flask import request
from flask import jsonify
from flask import send_from_directory, make_response
from flask import Blueprint
import os
import markdown
import pdfkit

from model import Note
from model import db

app = Blueprint("note", __name__, url_prefix='/note')


@app.route("/modifyNotes", methods=["POST"])
def modityNotes():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        newSourceCode = json["sourceCode"]
        note = Note.query.get(ID)
        if note==None:
            return jsonify({"status": "ERR"})
        note.sourceCode = newSourceCode
        db.session.commit()
        return jsonify({"status": "OK"})


@app.route("/previewNote", methods=["POST"])
def previewNote():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        note = Note.query.get(ID)
        if note==None:
            return jsonify({"status": "ERR"})
        return jsonify(markdown.markdown(note.sourceCode))


@app.route("/exportPDF", methods=["POST"])
def exportPDF():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        path = 'pdfGenerated/'
        fileName = ID + '.pdf'
        note = Note.query.get(ID)
        if note==None:
            return jsonify({"status": "ERR"})
        pdfkit.from_string(markdown.markdown(note.sourceCode), "test")
        return make_response(send_from_directory(os.path.join(app.root_path, path), fileName, as_attachment=True))


@app.route("/newNote", methods=["POST"])
def newNote():
    if request.method == "POST":
        json = request.get_json()
        newNote = Note(json["sourceCode"], json["owner"], json["course_belonged"])
        db.session.add(newNote)
        db.session.commit()
        return jsonify({"status": "OK"})


@app.route("/upVote", methods=["POST"])
def upVote():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        note = Note.query.get(ID)
        if note==None:
            return jsonify({"status": "ERR"})
        note.ups += 1
        db.session.commit()
        return jsonify({"status": "OK"})


@app.route("/downVote", methods=["POST"])
def downVote():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        note = Note.query.get(ID)
        if note==None:
            return jsonify({"status": "ERR"})
        note.ups -= 1
        db.session.commit()
        return jsonify({"status": "OK"})


@app.route("/getNote", methods=["POST"])
def getNote():
    if request.method == "POST":
        json = request.get_json()
        ID = json["ID"]
        note = Note.query.get(ID)
        if note==None:
            return jsonify({"status": "ERR"})
        return jsonify(
            {"sourceCode": note.sourceCode, "owner": note.owner, "createTime": note.createTime,
             "modifyTime": note.modifyTime, "courseBelonged": note.courseBelonged, "ups": note.ups})


@app.route("/getAllNoteID", methods=["GET"])
def getAllNoteID():
    if request.method == "GET":
        IDList = []
        for note in Note.query.all():
            IDList.append(note.id)
        return jsonify(IDList)
