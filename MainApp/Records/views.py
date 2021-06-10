from flask import Flask, render_template, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy  #SQL
from sqlalchemy import desc
from datetime import datetime, timedelta
from MainApp.database import db          #created database
from MainApp.models import Records
from MainApp.models import Items
from MainApp.models import Goals

def inputRecord(request):
    if request.method == 'GET':
        # show input page
        return render_template('records/record_input.html', items=Items.query.all())
    elif request.method == 'POST':
        # receive and handle input request
        # there's only ONE record with a particular combination (ItemNumber, Date, GoalNumber) in the database
        tupleToInsert = None

        itemNumber = request.form['itemNumber']
        date = request.form['date']
        duration = request.form['duration']
        goalNumber = request.form['goalNumber']
        achievePercentage = request.form['achievePercentage']
        description = request.form['description']

        if goalNumber == '':
            # make sure nullable attributes are NULL in the databse if user didn't type anything
            goalNumber = None
            achievePercentage = None
        else:
            # set achieve percentage to 0 if the user didn't enter anything in the achieve percentage input field
            if achievePercentage == '':
                achievePercentage = '0'

        result = Records.query.filter_by(ItemNumber=itemNumber, Date=date, GoalNumber=goalNumber).first()

        if result is None:
            # if no tuple was retrieved, create a new tuple
            tupleToInsert = Records(itemNumber, date, duration, goalNumber, achievePercentage, description)
        
        if tupleToInsert is not None:
            # if a new tuple was created, insert it
            db.session.execute('PRAGMA foreign_keys=ON') # enforce referential integrity constraints
            db.session.add(tupleToInsert)
            db.session.commit()

            if achievePercentage == '100':
                # if the user input '100' in the achieve percentage field, update the goal tuple
                goalToUpdate = Goals.query.filter_by(GoalNumber=goalNumber)
                if goalToUpdate.first().Achieved == 'N':
                    goalToUpdate.update({'Achieved': 'Y', 'AchieveDate': date})
                    db.session.commit()
                else:
                    # normally, this won't be executed
                    return 'The goal has already achieved'

            flash('The record was added successfully.')
            return redirect('/records/input')
        else:
            # else, show existied record fot that date
            if goalNumber is None:
                return render_template('records/record_existed.html', record=result)
            else:
                existedRecord = db.session.execute('SELECT Items.Category, Items.Name, Records.ItemNumber, Records.Date, Records.Duration, Goals.Goal, Records.AchievePercentage, Records.Description '+
                                                'FROM Items, Records, Goals '+
                                                'WHERE Records.ItemNumber = :it '+
                                                  'AND Records.Date = :dt '+
                                                  'AND Records.GoalNumber = :gn '+
                                                  'AND Records.ItemNumber = Items.ItemNumber '+
                                                  'AND Records.GoalNumber = Goals.GoalNumber',
                                                {'it': itemNumber, 'dt': date, 'gn':goalNumber}).first()
                return render_template('records/record_existed.html', record=existedRecord)


def generateAndReturnInJson(availableGoalsRawData):
    availableGoalsList = []

    # make an json object list of unfinished goals
    for a in availableGoalsRawData:
        dictionary = {
            'ItemName': a.ItemName,
            'GoalNumber': a.GoalNumber,
            'Goal': a.Goal
        }
        availableGoalsList.append(dictionary)
    
    return jsonify(availableGoalsList)



def input_getAvailableGoals(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']

        # retrieve unfinished goals
        availableGoalsRawData = db.session.execute('SELECT Items.Name AS ItemName, Goals.GoalNumber, Goals.Goal '+
                                            'FROM Items, Goals '+
                                            'WHERE Goals.ItemNumber = Items.ItemNumber '+
                                              'AND Goals.Achieved = "N" '+
                                              'AND Goals.ItemNumber = :it',
                                            {'it': itemNumber}).fetchall()
        
        return generateAndReturnInJson(availableGoalsRawData)



def listRecords():
    numberOfRecords = db.session.execute('SELECT COUNT(*) AS Number '+
                                         'FROM Records').fetchall()[0].Number
  
    if numberOfRecords > 0:
        recordDates = db.session.execute('SELECT Records.Date '+
                                        'FROM Records '+
                                        'ORDER BY Records.Date ASC').fetchall()

        oldest = recordDates[0].Date

        upperBoundDate = datetime.today()
        deltaDate = timedelta(days=7)

        upperBoundString = upperBoundDate.strftime("%Y-%m-%d")
        lowerBoundString = (upperBoundDate-deltaDate+timedelta(days=1)).strftime("%Y-%m-%d")

        numberOfRecordsInInterval = db.session.execute('SELECT COUNT(*) AS Number '+
                                                       'FROM Records '+
                                                       'WHERE Date >= :lb '+
                                                         'AND Date <= :ub',
                                                       {'lb': lowerBoundString, 'ub': upperBoundString}).fetchall()[0].Number

        orderedRecordSummary = []
        orderedRecords = []
        recordsBound = []

        while lowerBoundString >= oldest:
            if numberOfRecordsInInterval > 0:
                recordsInInterval = db.session.execute('SELECT Items.Category, Items.Name, Items.ItemNumber, Records.Date, Records.SetDateTime, Records.Duration, Goals.Goal, Records.AchievePercentage, Records.Description '+
                                                       'FROM ((Records LEFT OUTER JOIN Goals ON Records.GoalNumber = Goals.GoalNumber)'+
                                                               'JOIN Items ON Records.ItemNumber = Items.ItemNumber) '+
                                                       'WHERE Records.Date >= :lb AND Records.Date <= :ub '
                                                       'ORDER BY Records.Date DESC',
                                                       {'lb': lowerBoundString, 'ub': upperBoundString}).fetchall()
                
                recordSummaryInInterval = db.session.execute('SELECT Items.Name, SUM(Records.Duration) AS Total '+
                                                             'FROM Records, Items '+
                                                             'WHERE Records.ItemNumber = Items.ItemNumber '+
                                                               'AND Records.Date >= :lb AND Records.Date <= :ub '
                                                             'GROUP BY Records.ItemNumber',
                                                             {'lb': lowerBoundString, 'ub': upperBoundString}).fetchall()
                
                recordSummaryTemp = []
                for s in recordSummaryInInterval:
                    recordSummaryTemp.append(s)
                
                orderedRecordSummary.append(recordSummaryTemp)

                recordsTemp = []
                for r in recordsInInterval:
                    recordsTemp.append(r)
                
                orderedRecords.append(recordsTemp)
                recordsBound.append([lowerBoundString, upperBoundString])

            upperBoundDate = upperBoundDate - deltaDate

            upperBoundString = upperBoundDate.strftime("%Y-%m-%d")
            lowerBoundString = (upperBoundDate-deltaDate+timedelta(days=1)).strftime("%Y-%m-%d")

            numberOfRecordsInInterval = db.session.execute('SELECT COUNT(*) AS Number '+
                                                           'FROM Records '+
                                                           'WHERE Date >= :lb '+
                                                             'AND Date <= :ub',
                                                           {'lb': lowerBoundString, 'ub': upperBoundString}).fetchall()[0].Number

        
        return render_template('records/record_listAll.html', summary=orderedRecordSummary, records=orderedRecords, bound=recordsBound)
    else:
        return render_template('records/record_listAll.html')


def deleteRecord(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']
        setDateTime = request.form['setDateTime']

        tupleToDelete = Records.query.filter_by(ItemNumber=itemNumber, SetDateTime=setDateTime).first()

        if tupleToDelete is not None:
            if tupleToDelete.AchievePercentage == 100:
                goalNumberOfTuple = tupleToDelete.GoalNumber

                goalToUpdate = Goals.query.filter_by(GoalNumber=goalNumberOfTuple).first()
                if goalToUpdate.Achieved == 'Y':
                    goalToUpdate.Achieved = 'N'
                    goalToUpdate.AchieveDate = None
                    db.session.commit()

            db.session.delete(tupleToDelete)
            db.session.commit()

            flash('Deleted successfully.')
            return redirect('/records/listAll')
        else:
            flash('Error occured. Failed to delete record.')
            return redirect('/records/listAll')


def showRecordToModify(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']
        setDateTime = request.form['setDateTime']

        return render_template('records/record_modify.html', items=Items.query.all(), record=Records.query.filter_by(ItemNumber=itemNumber, SetDateTime=setDateTime).first())


def modify_getAvailableGoals(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']
        date = request.form['date']

        # retrieve the goals set before and achieved after the date of the record
        availableGoalsRawData = db.session.execute('SELECT Items.Name AS ItemName, Goals.GoalNumber, Goals.Goal '+
                                                   'FROM Items, Goals '+
                                                   'WHERE Goals.ItemNumber = Items.ItemNumber '+
                                                     'AND Goals.ItemNumber = :it '+
                                                     'AND Goals.SetDate <= :dt '+
                                                     'AND (Goals.AchieveDate >= :dt OR Goals.AchieveDate IS NULL)',
                                                   {'it': itemNumber, 'dt': date}).fetchall()

        return generateAndReturnInJson(availableGoalsRawData)


def modifyCheck(request):
    if request.method == 'POST':
        # there's only ONE record with a particular combination (ItemNumber, Date, GoalNumber) in the database
        itemNumber = request.form['itemNumber']
        date = request.form['date']
        goalNumber = request.form['goalNumber']

        originalItemNumber = request.form['originalItemNumber']
        originalDate = request.form['originalDate']
        originalGoalNumber = request.form['originalGoalNumber']

        if originalItemNumber == itemNumber and originalDate == date and originalGoalNumber == goalNumber:
            # if the user DIDN'T modify the ItemNumber, Date, and GoalNumber, 
            # the tuple is safe to be stored in the database
            return 'Y'
        else :
            # if the user DID modify the ItemNumber, Date, and GoalNumber, 
            # see if there's an record with a particular combination (ItemNumber, Date, GoalNumber) in the database
            result = Records.query.filter_by(ItemNumber=itemNumber, Date=date, GoalNumber=goalNumber).first()
            if result is None:
                # if there isn't a record for that day, it is safe to be stored in the database
                return 'Y'
            else:
                # otherwise, it is unsafe
                return 'The record for that day has already existed!'


def modifyRecord(request):
    if request.method == 'POST':
        # simply update the tuple
        tupleToUpdate = None

        itemNumber = request.form['itemNumber']
        date = request.form['date']
        duration = request.form['duration']
        goalNumber = request.form['goalNumber']
        achievePercentage = request.form['achievePercentage']
        description = request.form['description']
        setDateTime = request.form['setDateTime']

        originalItemNumber = request.form['originalItemNumber']

        if goalNumber == '':
            # make sure nullable attributes are NULL in the databse if user didn't type anything
            goalNumber = None
            achievePercentage = None
        else:
            # set achieve percentage to 0 if the user didn't enter anything in the achieve percentage input field
            if achievePercentage == '':
                achievePercentage = '0'

        tupleToUpdate = Records.query.filter_by(ItemNumber=originalItemNumber, SetDateTime=setDateTime).first()

        if tupleToUpdate is not None:
            tupleToUpdate.ItemNumber = itemNumber
            tupleToUpdate.Date = date
            tupleToUpdate.Duration = duration
            tupleToUpdate.GoalNumber = goalNumber
            tupleToUpdate.AchievePercentage = achievePercentage
            tupleToUpdate.Description = description

            db.session.commit()

            if achievePercentage == '100':
                # if the user input '100' in the achieve percentage field, update the goal tuple
                goalToUpdate = Goals.query.filter_by(GoalNumber=goalNumber).first()
                if goalToUpdate.Achieved == 'N':
                    goalToUpdate.Achieved = 'Y'
                    goalToUpdate.AchieveDate = date
                    db.session.commit()
            else:
                goalToUpdate = Goals.query.filter_by(GoalNumber=goalNumber).first()
                if goalToUpdate.Achieved == 'Y':
                    goalToUpdate.Achieved = 'N'
                    goalToUpdate.AchieveDate = None
                    db.session.commit()

            flash('Updated successfully.')
            return redirect('/records/listAll')
        else:
            flash('Error occured. Failed to update record.')
            return redirect('/records/listAll')