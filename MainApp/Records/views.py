from flask import Flask, render_template, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy  #SQL
from sqlalchemy import desc
from datetime import datetime, timedelta
import pandas as pd
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

        # make sure nullable attributes are NULL in the databse if user didn't type anything
        if goalNumber == '':
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

            goalToUpdate = Goals.query.filter_by(GoalNumber=goalNumber).first()
            
            if goalToUpdate is not None:
                achievePercentageRanking = db.session.execute('SELECT AchievePercentage '+
                                                             'FROM Records '+
                                                             'WHERE GoalNumber = :gn '+
                                                             'ORDER BY AchievePercentage DESC',
                                                             {'gn': goalNumber}).fetchall()
                
                if len(achievePercentageRanking) > 0:
                    goalToUpdate.AchievePercentage = achievePercentageRanking[0].AchievePercentage
                else:
                    goalToUpdate.AchievePercentage = 0

                if int(achievePercentage) >= 100:
                    # if the user input '100' in the achieve percentage field, update the goal tuple
                    if goalToUpdate.Achieved == 'N':
                        goalToUpdate.Achieved = 'Y'
                        goalToUpdate.AchieveDate = date
                    else:
                        # normally, this won't be executed
                        return 'The goal has already achieved'
                
                db.session.commit()

            flash('活動紀錄新增成功')
            return redirect('/records/input')
        else:
            # else, show existied record fot that date
            if goalNumber is None:
                return render_template('records/record_existed.html', record=result)
            else:
                existedRecord = db.session.execute('SELECT Items.Category, Items.Name, Records.ItemNumber, Records.Date, Records.Duration, Goals.Goal, Records.AchievePercentage, Records.Description, Records.SetDateTime '+
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
        num_days = 7

        recordDates = db.session.execute('SELECT Records.Date '+
                                        'FROM Records '+
                                        'ORDER BY Records.Date ASC').fetchall()

        oldest = recordDates[0].Date

        upperBoundDate = datetime.today()
        deltaDate = timedelta(days=num_days)

        upperBoundString = upperBoundDate.strftime("%Y-%m-%d")
        lowerBoundString = (upperBoundDate-deltaDate+timedelta(days=1)).strftime("%Y-%m-%d")

        numberOfRecordsInInterval = db.session.execute('SELECT COUNT(*) AS Number '+
                                                       'FROM Records '+
                                                       'WHERE Date >= :lb '+
                                                         'AND Date <= :ub',
                                                       {'lb': lowerBoundString, 'ub': upperBoundString}).fetchall()[0].Number

        intervalRecordSummary = []
        interval_dict_all_activity_7D = []
        intervalDate = []
        interval_dict_all_activity_sum_7D = []
        intervalRecords = []
        intervalBound = []

        while lowerBoundString >= oldest:
            if numberOfRecordsInInterval > 0:
                # by as0027111
                recordsInInterval = db.session.execute('SELECT Items.Category, Items.Name, Items.ItemNumber, Records.Date, Records.SetDateTime, Records.Duration, Goals.Goal, Records.AchievePercentage, Records.Description '+
                                                       'FROM ((Records LEFT OUTER JOIN Goals ON Records.GoalNumber = Goals.GoalNumber)'+
                                                               'JOIN Items ON Records.ItemNumber = Items.ItemNumber) '+
                                                       'WHERE Records.Date >= :lb AND Records.Date <= :ub '
                                                       'ORDER BY Records.Date DESC',
                                                       {'lb': lowerBoundString, 'ub': upperBoundString}).fetchall()
                record_df = pd.DataFrame(columns=['ItemName', 'Date', 'Duration', 'Content'])
                for i,data in enumerate(recordsInInterval):
                    record_df = record_df.append({  'ItemName': data.Name,
                                                    'Date': data.Date,
                                                    'Duration': data.Duration,
                                                    'Content': data.Description}, ignore_index=True)
                date_reord, time_record = course_statics(record_df.values)
                
                past = (upperBoundDate - timedelta(days=num_days-1)).strftime("%Y-%m-%d")
                date = [(datetime.strptime(past,'%Y-%m-%d')+timedelta(days=i)).strftime('%Y-%m-%d') for i in range(num_days)]
                dict_all_activity_7D, dict_all_activity_sum_7D = past_statics(past, date, num_days, date_reord, time_record)
                # by as0027111

                interval_dict_all_activity_7D.append(dict_all_activity_7D)
                intervalDate.append(date)
                interval_dict_all_activity_sum_7D.append(dict_all_activity_sum_7D)

                intervalRecordSummary.append(db.session.execute('SELECT Items.Category, SUM(Records.Duration) AS Total '+
                                                               'FROM Records, Items '+
                                                               'WHERE Records.ItemNumber = Items.ItemNumber '+
                                                                 'AND Records.Date >= :lb AND Records.Date <= :ub '+
                                                               'GROUP BY Items.Category '+
                                                               'ORDER BY Items.Category',
                                                               {'lb': lowerBoundString, 'ub': upperBoundString}).fetchall())

                recordsTemp = []
                for r in recordsInInterval:
                    recordsTemp.append(r)
                
                intervalRecords.append(recordsTemp)
                intervalBound.append([lowerBoundString, upperBoundString])

            upperBoundDate = upperBoundDate - deltaDate

            upperBoundString = upperBoundDate.strftime("%Y-%m-%d")
            lowerBoundString = (upperBoundDate-deltaDate+timedelta(days=1)).strftime("%Y-%m-%d")

            numberOfRecordsInInterval = db.session.execute('SELECT COUNT(*) AS Number '+
                                                           'FROM Records '+
                                                           'WHERE Date >= :lb '+
                                                             'AND Date <= :ub',
                                                           {'lb': lowerBoundString, 'ub': upperBoundString}).fetchall()[0].Number

        
        return render_template('records/record_listAll.html', \
            time_record=interval_dict_all_activity_7D, date=intervalDate, each_sum=interval_dict_all_activity_sum_7D,
            summary=intervalRecordSummary, records=intervalRecords, bound=intervalBound)
    else:
        return render_template('records/record_listAll.html')


# by as0027111
def course_statics(npdata):
    date = {}
    time = {}
    for i in npdata:
        if i[0] in time:
            date[i[0]].append(i[1])
            time[i[0]].append(i[2])
        else:
            date[i[0]] = [i[1]]
            time[i[0]] = [i[2]]
    return date, time


def past_statics(past, date, num_days, date_reord, time_record):
    dict_all_activity = {}
    dict_all_activity_sum = {}
    for i in time_record.keys():
        values = [0 for i in range(num_days)]
        d = date_reord[i]
        t = time_record[i]
        for j in range(len(d)):
            for k in range(len(date)):
                if d[j] == date[k]:
                    values[k] += t[j]
        dict_all_activity[i] = values
        dict_all_activity_sum[i] = sum(values)
    return dict_all_activity, dict_all_activity_sum
# by as0027111


def deleteRecord(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']
        setDateTime = request.form['setDateTime']

        tupleToDelete = Records.query.filter_by(ItemNumber=itemNumber, SetDateTime=setDateTime).first()

        if tupleToDelete is not None:
            goalNumber = tupleToDelete.GoalNumber
            achievePercentage = tupleToDelete.AchievePercentage

            db.session.delete(tupleToDelete)
            db.session.commit()

            goalToUpdate = Goals.query.filter_by(GoalNumber=goalNumber).first()

            if goalToUpdate is not None:
                achievePercentageRanking = db.session.execute('SELECT AchievePercentage '+
                                                              'FROM Records '+
                                                              'WHERE GoalNumber = :gn '+
                                                              'ORDER BY AchievePercentage DESC',
                                                              {'gn': goalNumber}).fetchall()
                
                if len(achievePercentageRanking) > 0:
                    goalToUpdate.AchievePercentage = achievePercentageRanking[0].AchievePercentage

                    if goalToUpdate.Achieved == 'Y' and achievePercentageRanking[0].AchievePercentage < 100:
                        goalToUpdate.Achieved = 'N'
                else:
                    goalToUpdate.AchievePercentage = 0

                if achievePercentage == 100:
                    goalToUpdate.Achieved = 'N'
                    goalToUpdate.AchieveDate = None
                    
                db.session.commit()

            flash('活動紀錄刪除成功')
            return redirect('/records/listAll')
        else:
            flash('發生未知的錯誤，無法刪除活動紀錄')
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
                return '已經有當天的紀錄了'


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
        originalGoalNumber = request.form['originalGoalNumber']

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

            goalToUpdate = Goals.query.filter_by(GoalNumber=goalNumber).first()

            if goalToUpdate is not None:
                if int(achievePercentage) >= 100:
                    # if the user input '100' in the achieve percentage field, update the goal tuple
                    if goalToUpdate.Achieved == 'N':
                        goalToUpdate.Achieved = 'Y'
                        goalToUpdate.AchievePercentage = achievePercentage
                        goalToUpdate.AchieveDate = date
                else:
                    achievePercentageRanking = db.session.execute('SELECT AchievePercentage '+
                                                                  'FROM Records '+
                                                                  'WHERE GoalNumber = :gn '+
                                                                  'ORDER BY AchievePercentage DESC',
                                                                  {'gn': goalNumber}).fetchall()
                    
                    if len(achievePercentageRanking) > 0:
                        goalToUpdate.AchievePercentage = achievePercentageRanking[0].AchievePercentage

                        if goalToUpdate.Achieved == 'Y' and achievePercentageRanking[0].AchievePercentage < 100:
                            goalToUpdate.Achieved = 'N'
                    else:
                        goalToUpdate.AchievePercentage = 0
                
                db.session.commit()
            else:
                goalToUpdate = Goals.query.filter_by(GoalNumber=originalGoalNumber).first()

                if goalToUpdate is not None:
                    achievePercentageRanking = db.session.execute('SELECT AchievePercentage '+
                                                                  'FROM Records '+
                                                                  'WHERE GoalNumber = :gn '+
                                                                  'ORDER BY AchievePercentage DESC',
                                                                  {'gn': originalGoalNumber}).fetchall()

                    if len(achievePercentageRanking) > 0:
                        goalToUpdate.AchievePercentage = achievePercentageRanking[0].AchievePercentage

                        if goalToUpdate.Achieved == 'Y' and achievePercentageRanking[0].AchievePercentage < 100:
                            goalToUpdate.Achieved = 'N'
                    else:
                        goalToUpdate.AchievePercentage = 0
                
                    db.session.commit()

            flash('活動紀錄更新成功')
            return redirect('/records/listAll')
        else:
            flash('發生未知的錯誤，無法更新活動紀錄')
            return redirect('/records/listAll')