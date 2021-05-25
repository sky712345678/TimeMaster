from flask import Flask                  #Flask
from flask import render_template        #rendering template
from flask_sqlalchemy import SQLAlchemy  #SQL
from sqlalchemy import desc
from MainApp.database import db          #created database
from MainApp.models import Records

def inputRecord(request):
    if request.method == 'GET':
        return render_template('items/item_input.html')
    elif request.method == 'POST':
        serialNumber = None
        date = None
        duration = None
        goal = None
        achievePercentage = None
        description = None
        
