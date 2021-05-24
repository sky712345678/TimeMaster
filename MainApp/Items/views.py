from flask import Flask                  #Flask
from flask import render_template        #rendering template
from flask_sqlalchemy import SQLAlchemy  #SQL
from sqlalchemy import desc
from MainApp.database import db          #created database
from MainApp.models import Items


def inputItem(request):
    category = None
    serialNumber = None
    name = None

    if request.method == 'GET':
        return render_template('items/item_input.html')
    elif request.method == 'POST':
        category = request.form['category']
        serialNumber = request.form['serialNumber']
        name = request.form['name']

        result = Items.query.filter_by(SerialNumber=serialNumber, Name=name).first()
        
        if result is None:
            if category == 'learning':
                tupleToInsert = Items(category, serialNumber, name)
            else:
                existedSerialNumber = Items.query.filter_by(Category=category).with_entities(Items.SerialNumber).order_by(desc(Items.SerialNumber))
                if existedSerialNumber.count() > 0:
                    latest = existedSerialNumber[0].SerialNumber
                    serialNumber = str(int(latest)+1).zfill(5)
                tupleToInsert = Items(category, serialNumber, name)
                # prevent user from inputing items with the same name
            db.session.add(tupleToInsert)
            db.session.commit()
            return '<h2>Successfully added.</h2>'
        else:
            return '<h2>Course already existed!!!</h2>'

def listItems():
    return render_template('items/item_listAll.html', items=Items.query.all())