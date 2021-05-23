from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy  #SQL
from MainApp.database import db          #created database
from MainApp.models import Courses       #include the table in database
from MainApp.models import Studies
from MainApp.models import Assignments
from MainApp.models import Tests
import pandas as pd
import random
from datetime import datetime, timedelta

app = Flask(__name__)

def test():
    start = '20210301'
    days = 120
    date = [(datetime.strptime(start,'%Y%m%d')+timedelta(days=i)).strftime('%Y%m%d') for i in range(days)]
    labels = ["January","February","March","April","May","June","July","August"]
    values = [random.randint(0,10) for i in range((len(date)))]
    values2 = [9, 4, 3, 8, 9, 6, 7, 6]
    return render_template('presentation/test.html', values=values, pass_labels=date, values2=values2)

def chart():
    result = db.session.execute('SELECT S.CourseNumber, C.CourseName, S.Date, S.Duration, S.Content '+
                                'FROM Studies AS S, Courses AS C '+
                                'WHERE S.CourseNumber=C.CourseNumber')
    course_df = pd.DataFrame(columns=['CourseNumber', 'CourseName', 'Date', 'Duration', 'Content'])
    for i,data in enumerate(result):
        course_df = course_df.append({'CourseNumber': data.CourseNumber,
                                    'CourseName':   data.CourseName,
                                    'Date':         data.Date,
                                    'Duration':     data.Duration,
                                    'Content':      data.Content}, ignore_index=True)
    print(course_df)
    date_reord, time_record = course_statics(course_df.values)
    print(date_reord, time_record)
    print("----------")                                
    
    return render_template('presentation/chart.html', studies=course_df.values, date=date_reord, time=time_record)

def choose(request):
    result = db.session.execute('SELECT S.CourseNumber, C.CourseName, S.Date, S.Duration, S.Content '+
                                'FROM Studies AS S, Courses AS C '+
                                'WHERE S.CourseNumber=C.CourseNumber')
    course_df = pd.DataFrame(columns=['CourseNumber', 'CourseName', 'Date', 'Duration', 'Content'])
    for i,data in enumerate(result):
        course_df = course_df.append({'CourseNumber': data.CourseNumber,
                                    'CourseName':   data.CourseName,
                                    'Date':         data.Date,
                                    'Duration':     data.Duration,
                                    'Content':      data.Content}, ignore_index=True)
    #print(course_df)
    date_reord, time_record = course_statics(course_df.values)
    print(date_reord, time_record)

    if request.method=='POST':
        choose_course = request.values['courseNumber']
        list_date = date_reord[choose_course]
        list_time = time_record[choose_course]
        list_date, list_time = (list(t) for t in zip(*sorted(zip(list_date, list_time))))
        list_date, list_time = learning_curve(list_date, list_time)
        print("The selected course", request.values['courseNumber'])
        return render_template('presentation/choose.html', courses=Courses.query.all(),
                            date=list_date, time=list_time)
    else:
        print("GGGGGGGGGGGGGGGGGG")
        return render_template('presentation/choose.html', courses=Courses.query.all(), date=None)

'''
list_date, list_time: the sorted studying record of one course
return learning curve like, date['20210301','20210302',...] 
                            values[0, 0, 0, 60, 60, 60, 180,...]
'''
def learning_curve(list_date, list_time):
    start = '20210301'
    num_days = 120
    date = [(datetime.strptime(start,'%Y%m%d')+timedelta(days=i)).strftime('%Y%m%d') for i in range(num_days)]
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
            date[i[0]].append(i[2])
            time[i[0]].append(i[3])
        else:
            date[i[0]] = [i[2]]
            time[i[0]] = [i[3]]
    return date, time
    

if __name__ == "__main__":
    app.run(host='127.0.0.2', port="5001", debug=True)

