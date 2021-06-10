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
import pandas as pd
import random
from datetime import datetime, timedelta
import time 
app = Flask(__name__)

def recent():
    num_days = 7
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
    print(date_reord, time_record)

    past = (datetime.today().date() - timedelta(days=num_days-1)).strftime("%Y-%m-%d")
    date = [(datetime.strptime(past,'%Y-%m-%d')+timedelta(days=i)).strftime('%Y-%m-%d') for i in range(num_days)]
    #print(date)
    dict_all_activity_7D, sum_7D, dict_all_activity_sum_7D = past_statics(7,date_reord,time_record)
    
    dict_all_activity_14D, sum_14D, dict_all_activity_sum_14D = past_statics(14,date_reord,time_record)
    #print(dict_all_activity_7D, sum_7D)
    #print(dict_all_activity_14D, sum_14D)
    print(dict_all_activity_sum_7D)
    print(dict_all_activity_sum_14D)
    compare = sum_7D - sum_14D
    return render_template('presentation/recent.html', items=Items.query.all(),
                time_record=dict_all_activity_7D, date=date, compare=compare, sum_7D=sum_7D, each_sum=dict_all_activity_sum_7D)

def past_statics(num_days,date_reord,time_record):
    past = (datetime.today().date() - timedelta(days=num_days-1)).strftime("%Y-%m-%d")
    date = [(datetime.strptime(past,'%Y-%m-%d')+timedelta(days=i)).strftime('%Y-%m-%d') for i in range(num_days)]
    dict_all_activity = {}
    dict_all_activity_sum = {}
    total_sum = 0
    for i in time_record.keys():
        values = [0 for i in range(num_days)]
        d = date_reord[i]
        t = time_record[i]
        for j in range(len(d)):
            for k in range(len(date)):
                if d[j] == date[k]:
                    values[k] += t[j]
                    total_sum += t[j]
        dict_all_activity[i] = values
        dict_all_activity_sum[i] = sum(values)
    return dict_all_activity, total_sum, dict_all_activity_sum

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
                print(presentation_all)
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

