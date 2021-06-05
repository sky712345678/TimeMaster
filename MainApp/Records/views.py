from flask import Flask, render_template, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy  #SQL
from sqlalchemy import desc
from MainApp.database import db          #created database
from MainApp.models import Records
from MainApp.models import Items
from MainApp.models import Goals

def inputRecord(request):
    if request.method == 'GET':
        availableGoals = db.session.execute('SELECT Items.Name AS ItemName, Goals.GoalNumber, Goals.Goal '+
                                            'FROM Items, Goals '+
                                            'WHERE Goals.ItemNumber = Items.ItemNumber '+
                                              'AND Goals.Achieved = "N"')
        return render_template('records/record_input.html', items=Items.query.all(), goals=availableGoals)
    elif request.method == 'POST':
        tupleToInsert = None

        itemNumber = request.form['itemNumber']
        date = request.form['date']
        duration = request.form['duration']
        goalNumber = request.form['goalNumber']
        achievePercentage = request.form['achievePercentage']
        description = request.form['description']

        result = Records.query.filter_by(ItemNumber=itemNumber, Date=date).first()

        # make sure nullable attributes are NULL if user didn't type anything
        if goalNumber == '':
            goalNumber = None
        if achievePercentage == '':
            achievePercentage = None

        if result is None:
            tupleToInsert = Records(itemNumber, date, duration, goalNumber, achievePercentage, description)
        
        if tupleToInsert is not None:
            db.session.execute('PRAGMA foreign_keys=ON')
            db.session.add(tupleToInsert)
            db.session.commit()

            if achievePercentage == '100':
                goalToUpdate = Goals.query.filter_by(GoalNumber=goalNumber)
                if goalToUpdate.first().Achieved == 'N':
                    goalToUpdate.update({'Achieved': 'Y', 'AchieveDate': date})
                    db.session.commit()
                else:
                    # normally, this won't be executed
                    return 'The goal has already achieved'

            flash('The record was added successfully')
            return redirect('/records/input')
        else:
            existedRecord = db.session.execute('SELECT Items.Name, Records.ItemNumber, Records.Date, Records.Duration, Goals.Goal, Records.AchievePercentage, Records.Description '+
                                               'FROM Items, Records, Goals '+
                                               'WHERE Records.ItemNumber = :it '+
                                                 'AND Records.Date = :dt '+
                                                 'AND Records.ItemNumber = Items.ItemNumber '+
                                                 'AND Records.GoalNumber = Goals.GoalNumber',
                                               {'it': itemNumber, 'dt': date}).first()
            return render_template('records/record_existed.html', record=existedRecord)
            


def input_getAvailableGoals(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']

        availableGoalsRawData = db.session.execute('SELECT Items.Name AS ItemName, Goals.GoalNumber, Goals.Goal '+
                                            'FROM Items, Goals '+
                                            'WHERE Goals.ItemNumber = Items.ItemNumber '+
                                              'AND Goals.Achieved = "N" '+
                                              'AND Goals.ItemNumber = :it',
                                            {'it': itemNumber}).fetchall()

        availableGoalsList = []

        for a in availableGoalsRawData:
            dictionary = {
                'ItemName': a.ItemName,
                'GoalNumber': a.GoalNumber,
                'Goal': a.Goal
            }

            availableGoalsList.append(dictionary)
        
        return jsonify(availableGoalsList)



def listRecords():
    numberOfRecords = db.session.execute('SELECT COUNT(*) AS Number '+
                                         'FROM Records').fetchall()[0].Number
    
    if numberOfRecords > 0:
        allRecords = db.session.execute('SELECT Items.Name, Items.ItemNumber, Records.Date, Records.Duration, Goals.Goal, Records.AchievePercentage, Records.Description '+
                                        # 'FROM Items, Records, Goals '+
                                        'FROM ((Records LEFT OUTER JOIN Goals ON Records.GoalNumber = Goals.GoalNumber)'+
                                                'JOIN Items ON Records.ItemNumber = Items.ItemNumber) '+
                                        'ORDER BY Records.Date DESC')
                                        # 'WHERE Records.ItemNumber = Items.ItemNumber')
                                          # 'AND Records.GoalNumber = Goals.GoalNumber')
        return render_template('records/record_listAll.html', records=allRecords)
    else:
        return '<h2>There isn\'t any record</h2>'


def deleteRecord(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']
        date = request.form['date']

        tupleToDelete = Records.query.filter_by(ItemNumber=itemNumber, Date=date).first()

        if tupleToDelete is not None:
            db.session.delete(tupleToDelete)
            db.session.commit()
            flash('Deleted successfully')
            return redirect('/records/listAll')
        else:
            flash('Error occured. Failed to delete record.')
            return redirect('/records/listAll')


def showRecordToModify(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']
        date = request.form['date']

        availableGoals = db.session.execute('SELECT Items.Name AS ItemName, Goals.GoalNumber, Goals.Goal '+
                                            'FROM Items, Goals '+
                                            'WHERE Goals.ItemNumber = Items.ItemNumber '+
                                              'AND Goals.SetDate <= :dt '+
                                              'AND (Goals.AchieveDate >= :dt OR Goals.AchieveDate IS NULL)',
                                            {'dt': date})

        return render_template('records/record_modify.html', items=Items.query.all(), goals=availableGoals, record=Records.query.filter_by(ItemNumber=itemNumber, Date=date).first())


def modifyRecord(request):
    if request.method == 'POST':
        tupleToUpdate = None

        itemNumber = request.form['itemNumber']
        date = request.form['date']
        duration = request.form['duration']
        goalNumber = request.form['goalNumber']
        achievePercentage = request.form['achievePercentage']
        description = request.form['description']

        originalItemNumber = request.form['originalItemNumber']
        originalDate = request.form['originalDate']

        if goalNumber == '':
            goalNumber = None
        
        if achievePercentage == '':
            achievePercentage = None

        tupleToUpdate = Records.query.filter_by(ItemNumber=originalItemNumber, Date=originalDate).first()

        if tupleToUpdate is not None:
            tupleToUpdate.ItemNumber = itemNumber
            tupleToUpdate.Date = date
            tupleToUpdate.Duration = duration
            tupleToUpdate.GoalNumber = goalNumber
            tupleToUpdate.AchievePercentage = achievePercentage
            tupleToUpdate.Description = description

            db.session.commit()

            flash('Updated successfully')
            return redirect('/records/listAll')
        else:
            flash('Error occured. Failed to update record.')
            return redirect('/records/listAll')