from flask import Flask                  #Flask
from flask import render_template        #rendering template
from flask_sqlalchemy import SQLAlchemy  #SQL
from sqlalchemy import desc
from MainApp.database import db          #created database
from MainApp.models import Records
from MainApp.models import Items
from MainApp.models import Goals

def inputRecord(request):
    if request.method == 'GET':
        return render_template('records/record_input.html', items=Items.query.all())
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
                if goalToUpdate.Achieved == 'N':
                    goalToUpdate.update({'Achieved': 'Y', 'AchieveDate': date})
                    db.session.commit()
                else:
                    return '<h2>The goal has already achieved'

            return '<h2>Successfully added.</h2>'
        else:
            existedRecord = db.session.execute('SELECT Items.Name, Records.Date, Records.Duration, Goals.Goal, Records.AchievePercentage, Records.Description '+
                                               'FROM Items, Records, Goals '+
                                               'WHERE Records.ItemNumber = :it '+
                                                 'AND Records.Date = :dt '+
                                                 'AND Records.ItemNumber = Items.ItemNumber '+
                                                 'AND Records.GoalNumber = Goals.GoalNumber',
                                               {'it': itemNumber, 'dt': date}).first()
            return render_template('records/record_existed.html', record=existedRecord)

def listRecords():
    allRecords = db.session.execute('SELECT Items.Name, Records.Date, Records.Duration, Goals.Goal, Records.AchievePercentage, Records.Description '+
                                  'FROM Items, Records '+
                                  'WHERE Records.ItemNumber = Items.ItemNumber '+
                                    'AND Records.GoalNumber = Goals.GoalNumber')
    return render_template('records/record_listAll.html', records=allRecords)