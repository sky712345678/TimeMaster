from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy  #SQL
from sqlalchemy import desc
from MainApp.database import db          #created database
from MainApp.models import Items


def inputItem(request):
    if request.method == 'GET':
        return render_template('items/item_input.html')

    elif request.method == 'POST':
        tupleToInsert = None

        category = request.form['category']
        itemNumber = request.form['itemNumber']
        name = request.form['name']
        
        if category == 'Learning':
            result = Items.query.filter_by(ItemNumber=itemNumber, Name=name).first()
            if result is None:
                tupleToInsert = Items(category, itemNumber, name)
        else:
            # existedSerialNumber = Items.query.filter_by(Category=category).with_entities(Items.SerialNumber).order_by(desc(Items.SerialNumber))
            result = Items.query.filter_by(Name=name).first()

            if result is None:
                numberOfNonLearningTuples = db.session.execute('SELECT COUNT (*) AS number '+
                                                                'FROM Items '+
                                                                'WHERE Category <> "Learning"').fetchall()[0].number
                
                if numberOfNonLearningTuples > 0:
                    existedItemNumber = db.session.execute('SELECT ItemNumber '+
                                                            'FROM Items '+
                                                            'WHERE Category <> "Learning" '+
                                                            'ORDER BY ItemNumber DESC').fetchall()
                    latest = existedItemNumber[0].ItemNumber
                    itemNumber = 'I'+str(int(latest[1:])+1).zfill(5)
                else:
                    itemNumber = 'I'+str(1).zfill(5)

                tupleToInsert = Items(category, itemNumber, name)
        
        if tupleToInsert is not None:
            db.session.add(tupleToInsert)
            db.session.commit()
            return 'Successfully added.'
        else:
            return 'Item already existed!'


def listItems():
    numberOfItems = db.session.execute('SELECT COUNT(*) AS Number '+
                                       'FROM Items').fetchall()[0].Number
    
    if numberOfItems > 0:
        return render_template('items/item_listAll.html', items=Items.query.all())
    else:
        return '<h2>There isn\'t any item</h2>'


def deleteItem(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']

        tupleToDelete = Items.query.filter_by(ItemNumber=itemNumber).first()

        if tupleToDelete is not None:
            db.session.delete(tupleToDelete)
            db.session.commit()
            return redirect('/items/listAll')
        else:
            return '<h2>Failed to delete item. Unknown error occured</h2>'