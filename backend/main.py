from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
import os

from configs import IMAGEPATH

app = Flask(__name__)
app.config.from_pyfile('configs.py')

@app.route("/")
def hello():
    return render_template('helloworld.html')

# db = SQLAlchemy(app)
# app.app_context().push()

if __name__ == "__main__":
    if not os.path.exists(IMAGEPATH):
        os.makedirs(IMAGEPATH)
    with app.app_context():
        from api import *
        # db.create_all()
        login_manager.init_app(app)
        app.register_blueprint(user_bp)
        app.register_blueprint(schedule_bp)
        app.register_blueprint(note_bp)
        app.register_blueprint(course_bp)
        app.run(debug=True)

