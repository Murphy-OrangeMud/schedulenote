from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
import os

from .configs import IMAGEPATH

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('configs.py')

    if not os.path.exists(IMAGEPATH):
        os.makedirs(IMAGEPATH)
    with app.app_context():
        from .api import login_manager, user_bp, schedule_bp, note_bp, course_bp, admin_bp
        # db.create_all()
        login_manager.init_app(app)
        app.register_blueprint(user_bp)
        app.register_blueprint(schedule_bp)
        app.register_blueprint(note_bp)
        app.register_blueprint(course_bp)
        app.register_blueprint(admin_bp)
    return app
