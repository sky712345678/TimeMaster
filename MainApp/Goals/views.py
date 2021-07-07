from flask import Flask, render_template, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy  #SQL
from sqlalchemy import desc
from MainApp.database import db          #created database
from MainApp.models import Goals
from MainApp.models import Items

def inputGoal(request):
    if request.method == 'GET':
        # show input page
        return render_template('goals/goal_input.html', items=Items.query.all())
    elif request.method == 'POST':
        # receive and handle input request
        # there's only ONE "unfinished" goal with a particular combination (ItemNumber, Goal) in the database
        tupleToInsert = None
        
        itemNumber = request.form['itemNumber']
        goal = request.form['goal']

        goal = goal.lower()

        result = Goals.query.filter_by(ItemNumber=itemNumber, Goal=goal, Achieved='N').first()

        if result is None:
            # if no tuple was retrieved, create a new tuple
            # generate a new goal number
            numberOfGoals = db.session.execute('SELECT COUNT (*) AS Number '+
                                               'FROM Goals').fetchall()[0].Number
            
            if numberOfGoals > 0:
                latest = db.session.execute('SELECT GoalNumber '+
                                            'FROM Goals '+
                                            'ORDER BY GoalNumber DESC').fetchall()[0].GoalNumber

                goalNumber = 'G'+str(int(latest[1:])+1).zfill(5)
            else:
                goalNumber = 'G'+str(1).zfill(5)
            
            tupleToInsert = Goals(goalNumber, itemNumber, goal)
        
        if tupleToInsert is not None:
            # if a new tuple was created, insert it
            db.session.execute('PRAGMA foreign_keys=ON') # enforce referential integrity constraints
            db.session.add(tupleToInsert)
            db.session.commit()

            flash('目標新增成功')
            return redirect('/goals/input')
        else:
            # else, show existied, unfinished goal
            existedGoal = db.session.execute('SELECT Items.ItemNumber, Items.Name, Items.Category, Goals.Goal, Goals.Achieved, Goals.SetDate, Goals.GoalNumber '+
                                              'FROM Items, Goals '+
                                              'WHERE Goals.ItemNumber = :in '+
                                                'AND Goals.Goal = :go '+
                                                'AND Goals.Achieved = "N" '+
                                                'AND Goals.ItemNumber = Items.ItemNumber',
                                              {'in': itemNumber, 'go': goal}).first()
            return render_template('goals/goal_existed.html', goal=existedGoal)
            


def listGoals():
    numberOfGoals = db.session.execute('SELECT COUNT(*) AS Number '+
                                       'FROM Goals').fetchall()[0].Number
    
    if numberOfGoals > 0:
        learningGoals = db.session.execute('SELECT Items.Category, Items.Name, Goals.ItemNumber, Goals.Goal, Goals.GoalNumber, Goals.Achieved, Goals.AchievePercentage, Goals.SetDate, Goals.AchieveDate '+
                                           'FROM Goals, Items '+
                                           'WHERE Goals.ItemNumber = Items.ItemNumber '+
                                             'AND Items.Category = "Learning"' +
                                           'ORDER BY Goals.Achieved ASC')
        sportsGoals = db.session.execute('SELECT Items.Category, Items.Name, Goals.ItemNumber, Goals.Goal, Goals.GoalNumber, Goals.Achieved, Goals.AchievePercentage, Goals.SetDate, Goals.AchieveDate '+
                                         'FROM Goals, Items '+
                                         'WHERE Goals.ItemNumber = Items.ItemNumber '+
                                           'AND Items.Category = "Sports"' +
                                         'ORDER BY Goals.Achieved ASC')
        leisureGoals = db.session.execute('SELECT Items.Category, Items.Name, Goals.ItemNumber, Goals.Goal, Goals.GoalNumber, Goals.Achieved, Goals.AchievePercentage, Goals.SetDate, Goals.AchieveDate '+
                                          'FROM Goals, Items '+
                                          'WHERE Goals.ItemNumber = Items.ItemNumber '+
                                            'AND Items.Category = "Leisure"' +
                                          'ORDER BY Goals.Achieved ASC')
        
        numberOfAchievedGoals = db.session.execute('SELECT COUNT (*) AS Number '+
                                                   'FROM Goals '+
                                                   'WHERE Goals.Achieved == "Y"').fetchall()[0].Number
        numberOfQuittedGoals = db.session.execute('SELECT COUNT (*) AS Number '+
                                                  'FROM Goals '+
                                                  'WHERE Goals.Achieved == "Q"').fetchall()[0].Number
        achievePercentage = int(float(numberOfAchievedGoals/numberOfGoals)*100)

        return render_template('goals/goal_listAll.html', learningGoals=learningGoals, sportsGoals=sportsGoals, \
                                leisureGoals=leisureGoals, numberOfAchievedGoals=numberOfAchievedGoals, \
                                numberOfQuittedGoals=numberOfQuittedGoals, numberOfGoals=numberOfGoals, \
                                percentage=achievePercentage)
    else:
        return render_template('goals/goal_listAll.html')


def quitGoal(request):
    if request.method == 'POST':
        goalNumber = request.form['goalNumber']

        tupleToQuit = Goals.query.filter_by(GoalNumber=goalNumber).first()

        if tupleToQuit is not None:
            tupleToQuit.Achieved = 'Q'
            db.session.commit()

            flash('目標已放棄')
            return redirect('/goals/listAll')
        else:
            flash('發生未知的錯誤，無法放棄目標')
            return redirect('/goals/listAll')


def deleteGoal(request):
    if request.method == 'POST':
        goalNumber = request.form['goalNumber']

        tupleToDelete = Goals.query.filter_by(GoalNumber=goalNumber).first()

        if tupleToDelete is not None:
            db.session.delete(tupleToDelete)
            db.session.commit()

            flash('目標刪除成功')
            return redirect('/goals/listAll')
        else:
            flash('發生未知的錯誤，無法刪除目標')
            return redirect('/goals/listAll')


def showGoalToModify(request):
    if request.method == 'POST':
        goalNumber = request.form['goalNumber']

        return render_template('goals/goal_modify.html', items=Items.query.all(), goal=Goals.query.filter_by(GoalNumber=goalNumber).first())


def modifyCheck(request):
    if request.method == 'POST':
        # there's only ONE unfinished goal with a particular combination (ItemNumber, Goal) in the database
        itemNumber = request.form['itemNumber']
        goal = request.form['goal']

        originalItemNumber = request.form['originalItemNumber']
        originalGoal = request.form['originalGoal']

        goal = goal.lower()

        if originalItemNumber == itemNumber and originalGoal == goal:
            # if the user DIDN'T modify the ItemNumber and Goal, the tuple is safe to be stored in the database
            return 'Y'
        else:
            # if the user DID modify the ItemNumber and Goal, 
            # see if there's an unfinished goal with a particular combination (ItemNumber, Goal) in the database
            result = Goals.query.filter_by(ItemNumber=itemNumber, Goal=goal, Achieved='N').first()
            if result is None:
                # if there isn't any unfinished goal, the tuple is safe to be stored in the database
                return 'Y'
            else:
                # otherwise, it is unsafe
                return '已經有這個目標了'


def modifyGoal(request):
    if request.method == 'POST':
        # simply update the tuple
        tupleToUpdate = None

        goalNumber = request.form['goalNumber']
        itemNumber = request.form['itemNumber']
        goal = request.form['goal']

        goal = goal.lower()

        tupleToUpdate = Goals.query.filter_by(GoalNumber=goalNumber).first()
        
        if tupleToUpdate is not None:
            tupleToUpdate.ItemNumber = itemNumber
            tupleToUpdate.Goal = goal

            db.session.commit()

            flash('目標更新成功')
            return redirect('/goals/listAll')
        else:
            flash('發生未知的錯誤，無法更新目標')
            return redirect('/goals/listAll')


def getPercentage(request):
    if request.method == 'POST':
        goalNumber = request.form['goalNumber']

        result = Goals.query.filter_by(GoalNumber=goalNumber).first()

        return str(result.AchievePercentage)