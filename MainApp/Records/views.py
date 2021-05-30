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
        '''
        serialNumber = None
        date = None
        duration = None
        goal = None
        achievePercentage = None
        setDate = None
        description = None
        '''

        tupleToInsert = None

        serialNumber = request.form['serialNumber']
        date = request.form['date']
        duration = request.form['duration']
        goal = request.form['goal']
        achievePercentage = request.form['achievePercentage']
        setDate = request.form['setDate']
        description = request.form['description']

        result = Records.query.filter_by(SerialNumber=serialNumber, Date=date).first()

        if goal == '':
            goal = None
        if setDate == '':
            setDate = None

        if result is None:
            tupleToInsert = Records(serialNumber, date, duration, goal, achievePercentage, setDate, description)
        
        if tupleToInsert is not None:
            db.session.execute('PRAGMA foreign_keys=ON')
            db.session.add(tupleToInsert)
            db.session.commit()

            if achievePercentage == '100':
                Goals.query.filter_by(SerialNumber=serialNumber, Goal=goal).update({'Achieved': 'Y', 'AchieveDate': date})
                db.session.commit()


            return '<h2>Successfully added.</h2>'
        else:
            existedRecord = db.session.execute('SELECT Items.Name, Records.Date, Records.Duration, Records.Goal, Records.AchievePercentage, Records.Description '+
                                               'FROM Items, Records '+
                                               'WHERE Records.SerialNumber = :sn '+
                                                 'AND Records.Date = :dt '+
                                                 'AND Records.SerialNumber = Items.SerialNumber',
                                               {'sn': serialNumber, 'dt': date}).first()
            return render_template('records/record_existed.html', record=existedRecord)

def listRecords():
    allRecords = db.session.execute('SELECT Items.Name, Records.Date, Records.Duration, Records.Goal, Records.AchievePercentage, Records.Description '+
                                  'FROM Items, Records '+
                                  'WHERE Items.SerialNumber = Records.SerialNumber')
    return render_template('records/record_listAll.html', records=allRecords)