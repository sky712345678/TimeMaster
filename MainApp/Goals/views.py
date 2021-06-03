from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy  #SQL
from sqlalchemy import desc
from MainApp.database import db          #created database
from MainApp.models import Goals
from MainApp.models import Items

def inputGoal(request):
    if request.method == 'GET':
        return render_template('goals/goal_input.html', items=Items.query.all())
    elif request.method == 'POST':
        tupleToInsert = None
        
        goalNumber = None
        itemNumber = request.form['itemNumber']
        goal = request.form['goal']

        result = Goals.query.filter_by(ItemNumber=itemNumber, Goal=goal, Achieved='N').first()

        # if no tuple is retrieved, create a new tuple
        if result is None:
            numberOfGoals = db.session.execute('SELECT COUNT (*) AS Number '+
                                               'FROM Goals').fetchall()[0].Number
            
            if numberOfGoals > 0:
                latest = db.session.execute('SELECT GoalNumber '+
                                            'FROM Goals '+
                                            'ORDER BY GoalNumber DESC').fetchall()[0].GoalNumber
                # latest = existedGoalNumber
                goalNumber = 'G'+str(int(latest[1:])+1).zfill(5)
            else:
                goalNumber = 'G'+str(1).zfill(5)
            
            tupleToInsert = Goals(goalNumber, itemNumber, goal)
        
        if tupleToInsert is not None:
            # if a new tuple is created, insert it
            db.session.execute('PRAGMA foreign_keys=ON')
            db.session.add(tupleToInsert)
            db.session.commit()
            return 'Successfully added.'
        else:
            # else, show existied, unfinished goal
            return 'Goal already existed!'
            '''
            existedGoal = db.session.execute('SELECT Items.Name, Goals.Goal, Goals.Achieved, Goals.SetDate '+
                                              'FROM Items, Goals '+
                                              'WHERE Goals.ItemNumber = :in '+
                                                'AND Goals.Goal = goal '+
                                                'AND Goals.Achieved = "N" '+
                                                'AND Goals.ItemNumber = Items.ItemNumber',
                                              {'in': itemNumber}).first()
            return render_template('goals/goal_existed.html', goal=existedGoal)
            '''


def listGoals():
    numberOfGoals = db.session.execute('SELECT COUNT(*) AS Number '+
                                       'FROM Goals').fetchall()[0].Number
    
    if numberOfGoals > 0:
        allGoals = db.session.execute('SELECT Items.Name, Goals.Goal, Goals.GoalNumber, Goals.Achieved, Goals.SetDate, Goals.AchieveDate '+
                                      'FROM Goals, Items '+
                                      'WHERE Goals.ItemNumber = Items.ItemNumber')
        return render_template('goals/goal_listAll.html', goals=allGoals)
    else:
        return '<h2>There isn\'t any set goal</h2>'


def deleteGoal(request):
    if request.method == 'POST':
        goalNumber = request.form['goalNumber']

        tupleToDelete = Goals.query.filter_by(GoalNumber=goalNumber).first()

        if tupleToDelete is not None:
            db.session.delete(tupleToDelete)
            db.session.commit()
            return redirect('/goals/listAll')
        else:
            return '<h2>Failed to delete item. Unknown error occured</h2>'