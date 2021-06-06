from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy  #SQL
from sqlalchemy import desc
from MainApp.database import db          #created database
from MainApp.models import Items


def inputCheck(request):
    if request.method == 'POST':
        category = request.form['category']
        itemNumber = request.form['itemNumber']
        name = request.form['name']

        name = name.lower()

        if category == 'Learning':
            if itemNumber != '':
                if '-' not in itemNumber or len(itemNumber) < 6:
                    return 'Please enter a valid course number with 6 digits'

            result = Items.query.filter_by(ItemNumber=itemNumber).first()

            if result is None:
                return 'Y'
            else:
                return 'The item has already existed!'
        else:
            result = Items.query.filter_by(Name=name).first()

            if result is None or result.Category != category:
                return 'Y'
            else:
                return 'The item has already existed!'
            

def inputItem(request):
    if request.method == 'GET':
        # show input page
        return render_template('items/item_input.html')
    elif request.method == 'POST':
        # receive and handle input request
        # if the catgory IS "Learning", there's only ONE item with a particular combination ItemNumber in the database
        # if the catgory ISN'T "Learning", there's only ONE item with a particular combination (Category, Name) in the database
        tupleToInsert = None

        category = request.form['category']
        itemNumber = request.form['itemNumber']
        name = request.form['name']

        name = name.lower()
        
        if category == 'Learning':
            result = Items.query.filter_by(ItemNumber=itemNumber).first()
            if result is None:
                # if no tuple was retrieved, create a new tuple
                tupleToInsert = Items(category, itemNumber, name)
        else:
            result = Items.query.filter_by(Name=name).first()

            if result is None or result.Category != category:
                # if no tuple was retrieved, create a new tuple
                # generate a new goal number
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

            flash('The item was added successfully.')
            return redirect('/items/input')
        else:
            flash('The item has already existed!')
            return redirect('/items/input')


def listItems():
    numberOfItems = db.session.execute('SELECT COUNT(*) AS Number '+
                                       'FROM Items').fetchall()[0].Number
    
    if numberOfItems > 0:
        return render_template('items/item_listAll.html', items=Items.query.all())
    else:
        return render_template('items/item_listAll.html')


def deleteItem(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']

        tupleToDelete = Items.query.filter_by(ItemNumber=itemNumber).first()

        if tupleToDelete is not None:
            db.session.delete(tupleToDelete)
            db.session.commit()

            flash('Deleted successfully.')
            return redirect('/items/listAll')
        else:
            flash('Error occured. Failed to delete item.')
            return redirect('/items/listAll')


def showItemToModify(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']

        return render_template('items/item_modify.html', item=Items.query.filter_by(ItemNumber=itemNumber).first())


def modifyCheck(request):
    if request.method == 'POST':
        category = request.form['category']
        itemNumber = request.form['itemNumber']
        name = request.form['name']

        originalCategory = request.form['originalCategory']
        originalItemNumber = request.form['originalItemNumber']
        originalName = request.form['originalName']

        name = name.lower()

        if category == 'Learning':
            # if the category is 'Learning'
            if originalCategory == category and originalItemNumber == itemNumber:
                # if the user DIDN'T edit the Category and ItemNumber, the tuple is safe to be stored in the database
                return 'Y'
            else:
                # else, check the ItemNumber and see if there's a tuple with the same ItemNumber
                if '-' not in itemNumber or len(itemNumber) < 6:
                    return 'Please enter a valid course number with 6 digits'
                else:
                    result = Items.query.filter_by(ItemNumber=itemNumber).first()

                    if result is None:
                        return 'Y'
                    else:
                        return 'The item has already existed!'
        elif category == 'Sports' or category == 'Leisure':
            # if the casegory isn't 'Learning'
            if originalCategory == category and originalName == name:
                # if the user DIDN'T edit the Category and Name, the tuple is safe to be stored in the database
                return 'Y'
            else:
                # else, see it there's a tuple with the same Category and Name
                result = Items.query.filter_by(Name=name).first()

                if result is None or result.Category != category:
                    return 'Y'
                else:
                    return 'The item has already existed!'


def modifyItem(request):
    if request.method == 'POST':
        tupleToUpdate = None

        category = request.form['category']
        itemNumber = request.form['itemNumber']
        name = request.form['name']

        originalCategory = request.form['originalCategory']
        originalItemNumber = request.form['originalItemNumber']

        name = name.lower()
        
        tupleToUpdate = Items.query.filter_by(ItemNumber=originalItemNumber).first()
        
        if tupleToUpdate is not None:
            tupleToUpdate.Name = name
            if originalCategory == category:
                tupleToUpdate.ItemNumber = itemNumber
            else:
                if (originalCategory == 'Sports' or originalCategory == 'Leisure') and category == 'Learning':
                    # if the category is changed from 'Sports' or 'Leisure' to 'Learning',
                    # assign the new course number
                    tupleToUpdate.ItemNumber = itemNumber
                elif originalCategory == 'Learning' and (category == 'Sports' or category == 'Leisure'):
                    # if the category is change from 'Learning' to 'Sports' or 'Leisure',
                    # generate a new item number
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
                    
                    tupleToUpdate.ItemNumber = itemNumber
                
                tupleToUpdate.Category = category

            db.session.commit()
            
            flash('Updated successfully.')
            return redirect('/items/listAll')
        else:
            flash('Error occured. Failed to update item.')
            return redirect('/items/listAll')