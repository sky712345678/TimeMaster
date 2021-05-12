import os
from datetime import datetime
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from MainApp import create
from MainApp.Learning import views as learning

app = create()

'''
app = Flask(__name__)
databasePath = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + databasePath + '/MainDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
'''

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/learning/CourseInput')
def course():
    return learning.course()

@app.route('/learning/CourseInput/submit', methods=['POST', 'GET'])
def inputCourse():
    return learning.inputCourse(request)

@app.route('/learning/ListCourses')
def listCourses():
    return learning.listAllCourses()

if __name__ == '__main__':
    app.run(debug=True)