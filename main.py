import os
from datetime import datetime
from flask import Flask, request, session, render_template
from flask_sqlalchemy import SQLAlchemy
from MainApp import create
from MainApp.Items import views as items_views
from MainApp.Records import views as records_views
from MainApp.Goals import views as goals_views
from MainApp import chart 

app = create()

@app.route('/')
def hello_world():
    return render_template('homepage.html')

@app.route('/items/input', methods=['POST', 'GET'])
@app.route('/items/input/submit', methods=['POST', 'GET'])
def items_input():
    return items_views.inputItem(request)

@app.route('/items/listAll')
def items_listAll():
    return items_views.listItems()

@app.route('/items/delete', methods=['POST', 'GET'])
def item_delete():
    return items_views.deleteItem(request)

@app.route('/goals/input', methods=['POST', 'GET'])
@app.route('/goals/input/submit', methods=['POST', 'GET'])
def goals_input():
    return goals_views.inputGoal(request)

@app.route('/goals/listAll')
def goals_listAll():
    return goals_views.listGoals()

@app.route('/goals/delete', methods=['POST', 'GET'])
def goals_delete():
    return goals_views.deleteGoal(request)

@app.route('/records/input', methods=['POST', 'GET'])
@app.route('/records/input/submit', methods=['POST', 'GET'])
def records_input():
    return records_views.inputRecord(request)

@app.route('/records/listAll')
def records_listAll():
    return records_views.listRecords()

@app.route('/records/delete', methods=['POST', 'GET'])
def records_delete():
    return records_views.deleteRecord(request)

@app.route('/presentation/test')
def test_chart():
    return chart.test()

@app.route('/presentation/chart')
def check_chart():
    return chart.chart()

@app.route('/presentation/choose', methods=['POST', 'GET'])
def choose_chart():
    return chart.choose(request)

'''
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

@app.route('/learning/Test/input')
def test():
    return learning.test()

@app.route('/learning/Test/input/submit', methods=['POST', 'GET'])
def inputTest():
    return learning.inputTest(request)

@app.route('/learning/Test/listAll')
def listTests():
    return learning.listAllTests()

@app.route('/learning/Assignment/input')
def assignment():
    return learning.assignment()

@app.route('/learning/Assignment/input/submit', methods=['POST', 'GET'])
def inputAssignment():
    return learning.inputAssignment(request)

@app.route('/learning/Assignment/listAll')
def listAssignments():
    return learning.listAllAssignments()
'''

if __name__ == '__main__':
    app.run(debug=True)