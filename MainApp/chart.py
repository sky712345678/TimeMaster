from flask import Flask
from flask import jsonify
from flask import render_template
from flask_sqlalchemy import SQLAlchemy  #SQL
from MainApp.database import db          #created database
# from MainApp.models import Courses       #include the table in database
# from MainApp.models import Studies
# from MainApp.models import Assignments
# from MainApp.models import Tests
from MainApp.models import Items
from MainApp.models import Goals
from MainApp.models import Records
import pandas as pd
import random
from datetime import datetime, timedelta
import time 
app = Flask(__name__)

def recent():
    # deal with the data passed to chart.js
    num_days = 7
    allRecords = db.session.execute('SELECT Items.Category, Items.Name, Items.ItemNumber, Records.Date, Records.SetDateTime, Records.Duration, Goals.Goal, Records.AchievePercentage, Records.Description '+
                                        'FROM ((Records LEFT OUTER JOIN Goals ON Records.GoalNumber = Goals.GoalNumber)'+
                                                'JOIN Items ON Records.ItemNumber = Items.ItemNumber) '+
                                        'ORDER BY Records.Date DESC') # select all record
    record_df = pd.DataFrame(columns=['ItemName', 'Date', 'Duration', 'Content'])
    for i,data in enumerate(allRecords):
        record_df = record_df.append({  'ItemName': data.Name,
                                        'Date': data.Date,
                                        'Duration': data.Duration,
                                        'Content': data.Description}, ignore_index=True)
    date_reord, time_record = course_statics(record_df.values)
    #print(date_reord, time_record)
    
    past = (datetime.today().date() - timedelta(days=num_days-1)).strftime("%Y-%m-%d")
    date = [(datetime.strptime(past,'%Y-%m-%d')+timedelta(days=i)).strftime('%Y-%m-%d') for i in range(num_days)]
    #print(date)
    dict_all_activity_7D, dict_all_activity_sum_7D = past_statics(7,date_reord,time_record)
    # deal with the staticial info of category 
    today = (datetime.today().date()).strftime("%Y-%m-%d")
    past_7D = (datetime.today().date() - timedelta(days=num_days-1)).strftime("%Y-%m-%d")
    past_14D = (datetime.today().date() - timedelta(days=num_days-1)).strftime("%Y-%m-%d")
    category_sum = db.session.execute('SELECT Items.Category, SUM(Records.Duration) '+
                                        'FROM ((Records LEFT OUTER JOIN Goals ON Records.GoalNumber = Goals.GoalNumber)'+
                                                'JOIN Items ON Records.ItemNumber = Items.ItemNumber) '+
                                        'WHERE Records.Date >= :lb AND Records.Date <= :ub '+
                                        'GROUP BY Items.Category '+ 
                                        'ORDER BY Records.Date DESC',
                                        {'lb':past_7D, 'ub':today})
    category_sum_14D = db.session.execute('SELECT Items.Category, SUM(Records.Duration) '+
                                        'FROM ((Records LEFT OUTER JOIN Goals ON Records.GoalNumber = Goals.GoalNumber)'+
                                                'JOIN Items ON Records.ItemNumber = Items.ItemNumber) '+
                                        'WHERE Records.Date >= :lb AND Records.Date <= :ub '+
                                        'GROUP BY Items.Category '+ 
                                        'ORDER BY Records.Date DESC',
                                        {'lb':past_14D, 'ub':past_7D})

    # modified by sky712345678
    recentRecords = db.session.execute('SELECT Items.Category, Items.Name, Items.ItemNumber, Records.Date, Records.SetDateTime, Records.Duration, Goals.Goal, Records.AchievePercentage, Records.Description '+
                                        'FROM ((Records LEFT OUTER JOIN Goals ON Records.GoalNumber = Goals.GoalNumber)'+
                                                'JOIN Items ON Records.ItemNumber = Items.ItemNumber) '+
                                        'WHERE Records.Date >= :lb AND Records.Date <= :ub '
                                        'ORDER BY Records.Date DESC',
                                        {'lb': past_7D, 'ub': today}).fetchall()

    numberOfGoals = db.session.execute('SELECT COUNT(*) AS Number '+
                                       'FROM Goals').fetchall()[0].Number

    numberOfAchievedGoals = db.session.execute('SELECT COUNT (*) AS Number '+
                                                'FROM Goals '+
                                                'WHERE Goals.Achieved == "Y"').fetchall()[0].Number
    numberOfQuittedGoals = db.session.execute('SELECT COUNT (*) AS Number '+
                                                'FROM Goals '+
                                                'WHERE Goals.Achieved == "Q"').fetchall()[0].Number
    achievePercentage = int(float(numberOfAchievedGoals/numberOfGoals)*100)

    recentGoals = db.session.execute('SELECT Items.Category, Items.Name, Goals.ItemNumber, Goals.Goal, Goals.GoalNumber, Goals.Achieved, Goals.SetDate, Goals.AchieveDate '+
                                    'FROM Goals, Items '+
                                    'WHERE Goals.ItemNumber = Items.ItemNumber '+
                                        'AND Goals.SetDate >= :lb AND Goals.SetDate <= :ub '+
                                    'ORDER BY Goals.Achieved, Goals.SetDate ASC',
                                    {'lb': past_7D, 'ub': today}).fetchall()

    frequentItems = db.session.execute('SELECT * '+
                                       'FROM Items '+
                                       'WHERE Items.ItemNumber IN ('+
                                            'SELECT ItemNumber '+
                                            'FROM ('
                                                'SELECT Records.ItemNumber, SUM(Records.Duration) AS Time '+
                                                'FROM Records '+
                                                'GROUP BY Records.ItemNumber '+
                                                'ORDER BY Time DESC '+
                                                'LIMIT 0, 3) AS TimeSpentRanking)').fetchall()
    
    # modified by sky712345678

    return render_template('presentation/recent.html', items=Items.query.all(), zip=zip,
                time_record=dict_all_activity_7D, date=date, each_sum=dict_all_activity_sum_7D,
                category_sum=category_sum, category_sum_14D=category_sum_14D,
                # modified by sky712345678
                recentRecords=recentRecords, recentGoals=recentGoals, 
                numberOfAchievedGoals=numberOfAchievedGoals, numberOfQuittedGoals=numberOfQuittedGoals,
                numberOfGoals=numberOfGoals, percentage=achievePercentage,
                frequentItems=frequentItems)
                # modified by sky712345678

'''
Turn the record to wanted format :
date_reord: {'database system': ['2021-06-07', '2021-05-07'], 'cycling': ['2021-06-07']}
time_record: {'database system': [175, 120], 'cycling': [60]}
dict_all_activity: {'database system':[0, 0, 0, 0, 175, 0, 0], 'cycling':...}
dict_all_activity_sum: {'database system':295, 'cycling':60}
'''
def past_statics(num_days,date_reord,time_record):
    past = (datetime.today().date() - timedelta(days=num_days-1)).strftime("%Y-%m-%d")
    date = [(datetime.strptime(past,'%Y-%m-%d')+timedelta(days=i)).strftime('%Y-%m-%d') for i in range(num_days)]
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

def chart(request):
    if request.method=='POST':
        choose_item = request.values['item_name']
        numberOfRecords = db.session.execute('SELECT COUNT(*) AS Number '+
                                            'FROM Records').fetchall()[0].Number
        
        if numberOfRecords > 0:
            allRecords = db.session.execute('SELECT Items.Category, Items.Name, Items.ItemNumber, Records.Date, Records.SetDateTime, Records.Duration, Goals.Goal, Records.AchievePercentage, Records.Description '+
                                        'FROM ((Records LEFT OUTER JOIN Goals ON Records.GoalNumber = Goals.GoalNumber)'+
                                                'JOIN Items ON Records.ItemNumber = Items.ItemNumber) '+
                                        'ORDER BY Records.Date DESC')
                                            # 'WHERE Records.ItemNumber = Items.ItemNumber')
                                            # 'AND Records.GoalNumber = Goals.GoalNumber')
            record_df = pd.DataFrame(columns=['ItemName', 'Date', 'Duration', 'Content'])
            for i,data in enumerate(allRecords):
                record_df = record_df.append({  'ItemName': data.Name,
                                                'Date': data.Date,
                                                'Duration': data.Duration,
                                                'Content': data.Description}, ignore_index=True)
            date_reord, time_record = course_statics(record_df.values)
            if choose_item == 'All':
                presentation_all = {}
                for i in time_record.keys():
                    d = date_reord[i]
                    t = time_record[i]
                    l_d, l_t = learning_curve(d, t)
                    presentation_all[i] = l_t
                #print(presentation_all)
                return render_template('presentation/choose_ALL.html', items=Items.query.all(),
                            time_record=presentation_all, date =l_d)
            else:
                list_date = date_reord[choose_item]
                list_time = time_record[choose_item]
                list_date, list_time = learning_curve(list_date, list_time)
                print(list_date, list_time)
            
                print("The selected course:", choose_item)
                return render_template('presentation/choose.html', items=Items.query.all(),
                                date=list_date, time=list_time, selected_item=choose_item)
    else:
        #print(Items.query.all())
        return render_template('presentation/choose.html', items=Items.query.all(), selected_item=None,
                            date=None, time=None)


'''
list_date, list_time: the sorted studying record of one course
return learning curve like, date['20210301','20210302',...] 
                            values[0, 0, 0, 60, 60, 60, 180,...]
'''
def learning_curve(list_date, list_time, start = '2021-03-01', num_days = 140):
    
    
    date = [(datetime.strptime(start,'%Y-%m-%d')+timedelta(days=i)).strftime('%Y-%m-%d') for i in range(num_days)]
    values = [0 for i in range(num_days)]
    for i in range(1, num_days):
        for j in range(len(list_date)):
            if date[i] == list_date[j]:
                values[i] = list_time[j] + values[i-1]
                break
            else:
                values[i] = values[i-1]
    return date, values
                


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
    

if __name__ == "__main__":
    app.run(host='127.0.0.2', port="5001", debug=True)

