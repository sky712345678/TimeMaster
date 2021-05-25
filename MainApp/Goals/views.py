from flask import Flask                  #Flask
from flask import render_template        #rendering template
from flask_sqlalchemy import SQLAlchemy  #SQL
from sqlalchemy import desc
from MainApp.database import db          #created database
from MainApp.models import Goals
from MainApp.models import Items

def inputGoal(request):
    if request.method == 'GET':
        return render_template('goals/goal_input.html', items=Items.query.all())
    elif request.method == 'POST':
        serialNumber = None
        goal = None

        tupleToInsert = None

        serialNumber = request.form['serialNumber']
        goal = request.form['goal']

        result = Goals.query.filter_by(SerialNumber=serialNumber, Goal=goal, Achieved='N').first()

        if result is None:
            tupleToInsert = Goals(serialNumber, goal)
        
        if tupleToInsert is not None:
            db.session.add(tupleToInsert)
            db.session.commit()
            return '<h2>Successfully added.</h2>'
        else:
            existingGoal = db.session.execute('SELECT Items.Name, Goals.Goal, Goals.Achieved, Goals.SetDate '+
                                              'FROM Items, Goals '+
                                              'WHERE Goals.SerialNumber = :sn '+
                                                'AND Goals.Goal = goal '+
                                                'AND Goals.Achieved = "N" '+
                                                'AND Goals.SerialNumber = Items.SerialNumber',
                                              {'sn': serialNumber}).first()
            return render_template('goals/goal_existed.html', goal=existingGoal)

def listGoals():
    allGoals = db.session.execute('SELECT Items.Name, Goals.Goal, Goals.Achieved, Goals.SetDate, Goals.AchieveDate '+
                                  'FROM Goals, Items '+
                                  'WHERE Goals.SerialNumber = Items.SerialNumber')
    return render_template('goals/goal_listAll.html', goals=allGoals)