# 临时文件，用于生成和测试日历部分。后续需要合并

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test2.db'

@app.route('/')
def my_chart():
    return render_template('helloworld.html')

if __name__ == "__main__":
    with app.app_context():
        import data
        app.register_blueprint(data.app)
        app.run(debug=True)