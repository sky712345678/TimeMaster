import os
from datetime import datetime
from flask import Flask, request, session, render_template
from flask_sqlalchemy import SQLAlchemy
from MainApp import create
from MainApp.Items import views as items_views
from MainApp.Records import views as records_views
from MainApp.Goals import views as goals_views
from MainApp import home

app = create()
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/home')
def recent():
    return home.recent()

@app.route('/items/input/check', methods=['POST', 'GET'])
def items_input_check():
    return items_views.inputCheck(request)

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

@app.route('/items/modify', methods=['POST', 'GET'])
def item_modify():
    return items_views.showItemToModify(request)

@app.route('/items/modify/check', methods=['POST', 'GET'])
def item_modify_check():
    return items_views.modifyCheck(request)

@app.route('/items/modify/submit', methods=['POST', 'GET'])
def item_modify_submit():
    return items_views.modifyItem(request)

@app.route('/goals/input', methods=['POST', 'GET'])
@app.route('/goals/input/submit', methods=['POST', 'GET'])
def goals_input():
    return goals_views.inputGoal(request)

@app.route('/goals/listAll')
def goals_listAll():
    return goals_views.listGoals()

@app.route('/goals/quit', methods=['POST', 'GET'])
def goals_quit():
    return goals_views.quitGoal(request)

@app.route('/goals/delete', methods=['POST', 'GET'])
def goals_delete():
    return goals_views.deleteGoal(request)

@app.route('/goals/modify', methods=['POST', 'GET'])
def goals_modify():
    return goals_views.showGoalToModify(request)

@app.route('/goals/modify/check', methods=['POST', 'GET'])
def goals_modify_check():
    return goals_views.modifyCheck(request)

@app.route('/goals/modify/submit', methods=['POST', 'GET'])
def goals_modify_submit():
    return goals_views.modifyGoal(request)

@app.route('/goals/get_percentage', methods=['POST', 'GET'])
def goals_get_percentage():
    return goals_views.getPercentage(request)

@app.route('/records/input', methods=['POST', 'GET'])
@app.route('/records/input/submit', methods=['POST', 'GET'])
def records_input():
    return records_views.inputRecord(request)

@app.route('/records/input/getAvailableGoals', methods=['POST', 'GET'])
def records_input_getAvailableGoals():
    return records_views.input_getAvailableGoals(request)

@app.route('/records/listAll')
def records_listAll():
    return records_views.listRecords()

@app.route('/records/delete', methods=['POST', 'GET'])
def records_delete():
    return records_views.deleteRecord(request)

@app.route('/records/modify', methods=['POST', 'GET'])
def records_modify():
    return records_views.showRecordToModify(request)

@app.route('/records/modify/getAvailableGoals', methods=['POST', 'GET'])
def records_modify_getAvailableGoals():
    return records_views.modify_getAvailableGoals(request)

@app.route('/records/modify/check', methods=['POST', 'GET'])
def records_modify_check():
    return records_views.modifyCheck(request)

@app.route('/records/modify/submit', methods=['POST', 'GET'])
def records_modify_submit():
    return records_views.modifyRecord(request)

@app.route('/presentation/chart', methods=['POST', 'GET'])
def check_chart():
    return home.chart(request)


if __name__ == '__main__':
    app.run()