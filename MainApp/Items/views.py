from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy  #SQL
from sqlalchemy import desc
from MainApp.database import db          #created database
from MainApp.models import Items
from MainApp.models import Records


def inputCheck(request):
    if request.method == 'POST':
        result = None

        category = request.form['category']
        itemNumber = request.form['itemNumber']
        learningOption = request.form['learningOption']
        name = request.form['name']

        name = name.lower()

        if category == 'Learning' and learningOption == 'yes':
            if '-' not in itemNumber or len(itemNumber) < 6:
                return '請輸入有效的課程代號'

            result = Items.query.filter_by(ItemNumber=itemNumber).first()

            if result is None:
                return 'Y'
            else:
                return '已經有這個項目了'
        else:
            result = Items.query.filter_by(Name=name).first()

            if result is None or result.Category != category:
                return 'Y'
            else:
                return '已經有這個項目了'
            

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
        learningOption = request.form['learningOption']
        name = request.form['name']

        name = name.lower()
        
        if category == 'Learning' and learningOption == 'yes':
            tupleToInsert = Items(category, itemNumber, name)
        else:
            numberOfNonLearningTuples = db.session.execute('SELECT COUNT (*) AS number '+
                                                            'FROM Items '+
                                                            'WHERE ItemNumber NOT LIKE "%-%"').fetchall()[0].number
            
            if numberOfNonLearningTuples > 0:
                existedItemNumber = db.session.execute('SELECT ItemNumber '+
                                                        'FROM Items '+
                                                        'WHERE ItemNumber NOT LIKE "%-%" '+
                                                        'ORDER BY ItemNumber DESC').fetchall()
                latest = existedItemNumber[0].ItemNumber
                itemNumber = 'I'+str(int(latest[1:])+1).zfill(5)
            else:
                itemNumber = 'I'+str(1).zfill(5)

            tupleToInsert = Items(category, itemNumber, name)
        
        if tupleToInsert is not None:
            db.session.add(tupleToInsert)
            db.session.commit()

            flash('項目新增程動')
            return redirect('/items/input')
        else:
            flash('已有重複的項目')
            return redirect('/items/input')


def listItems():
    numberOfItems = db.session.execute('SELECT COUNT(*) AS Number '+
                                       'FROM Items').fetchall()[0].Number
    
    if numberOfItems > 0:
        return render_template('items/item_listAll.html', learningItems=Items.query.filter_by(Category='Learning'), \
                                sportsItems=Items.query.filter_by(Category='Sports'), leisureItems=Items.query.filter_by(Category='Leisure'))
    else:
        return render_template('items/item_listAll.html')


def deleteItem(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']

        tupleToDelete = Items.query.filter_by(ItemNumber=itemNumber).first()

        if tupleToDelete is not None:
            db.session.delete(tupleToDelete)
            db.session.commit()

            flash('項目刪除成功')
            return redirect('/items/listAll')
        else:
            flash('發生未知的錯誤，無法刪除項目')
            return redirect('/items/listAll')


def showItemToModify(request):
    if request.method == 'POST':
        itemNumber = request.form['itemNumber']

        return render_template('items/item_modify.html', item=Items.query.filter_by(ItemNumber=itemNumber).first())


def modifyCheck(request):
    if request.method == 'POST':
        category = request.form['category']
        itemNumber = request.form['itemNumber']
        learningOption = request.form['learningOption']
        name = request.form['name']

        originalCategory = request.form['originalCategory']
        originalItemNumber = request.form['originalItemNumber']
        originalName = request.form['originalName']

        name = name.lower()

        if category == 'Learning':
            # if the category is 'Learning'
            if learningOption == 'yes':
                if originalCategory == category and originalItemNumber == itemNumber:
                    # if the user DIDN'T edit the Category and ItemNumber, the tuple is safe to be stored in the database
                    return 'Y'
                else:
                    # else, check the ItemNumber and see if there's a tuple with the same ItemNumber
                    if '-' not in itemNumber or len(itemNumber) < 6:
                        return '請輸入有效的課程代號'
                    else:
                        result = Items.query.filter_by(ItemNumber=itemNumber).first()

                        if result is None:
                            return 'Y'
                        else:
                            return '已經有這個項目了'
            else:
                if originalCategory == category and originalName == name:
                    return 'Y'
                else:
                    result = Items.query.filter_by(Name=name).first()

                    if result is None or result.Category != category:
                        return 'Y'
                    else:
                        return '已經有這個項目了'
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
                    return '已經有這個項目了'


def modifyItem(request):
    if request.method == 'POST':
        tupleToUpdate = None

        category = request.form['category']
        itemNumber = request.form['itemNumber']
        learningOption = request.form['learningOption']
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
                    if learningOption == 'yes':
                        tupleToUpdate.ItemNumber = itemNumber
                elif originalCategory == 'Learning' and (category == 'Sports' or category == 'Leisure'):
                    # if the category is change from 'Learning' to 'Sports' or 'Leisure',
                    # generate a new item number
                    if '-' in originalItemNumber:
                        numberOfNonLearningTuples = db.session.execute('SELECT COUNT (*) AS number '+
                                                                        'FROM Items '+
                                                                        'WHERE ItemNumber NOT LIKE "%-%"').fetchall()[0].number
                        
                        if numberOfNonLearningTuples > 0:
                            existedItemNumber = db.session.execute('SELECT ItemNumber '+
                                                                    'FROM Items '+
                                                                    'WHERE ItemNumber NOT LIKE "%-%" '+
                                                                    'ORDER BY ItemNumber DESC').fetchall()
                            latest = existedItemNumber[0].ItemNumber
                            itemNumber = 'I'+str(int(latest[1:])+1).zfill(5)
                        else:
                            itemNumber = 'I'+str(1).zfill(5)
                        
                        tupleToUpdate.ItemNumber = itemNumber
                
                tupleToUpdate.Category = category

            db.session.commit()
            
            flash('項目更新成功')
            return redirect('/items/listAll')
        else:
            flash('發生未知的錯誤，無法更新項目')
            return redirect('/items/listAll')