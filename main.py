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

@app.route('/learning/Course/input')
def course():
    return learning.course()

@app.route('/learning/Course/input/submit', methods=['POST', 'GET'])
def inputCourse():
    return learning.inputCourse(request)

@app.route('/learning/Course/listAll')
def listCourses():
    return learning.listAllCourses()

@app.route('/learning/Study/input')
def study():
    return learning.study()

@app.route('/learning/Study/input/submit', methods=['POST', 'GET'])
def inputStudy():
    return learning.inputStudy(request)

@app.route('/learning/Study/listAll')
def listStudies():
    return learning.listAllStudies()

@app.route('/learning/Assignment/input')
def assignment():
    return learning.assignment()

@app.route('/learning/Assignment/input/submit', methods=['POST', 'GET'])
def inputAssignment():
    return learning.inputAssignment(request)

@app.route('/learning/Assignment/listAll')
def listAssignments():
    return learning.listAllAssignments()


if __name__ == '__main__':
    app.run(debug=True)