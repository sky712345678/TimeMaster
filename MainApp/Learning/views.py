from flask import Flask                  #Flask
from flask import render_template        #rendering template
from flask_sqlalchemy import SQLAlchemy  #SQL
from MainApp.database import db          #created database
from MainApp.models import Courses       #include the table in database
from MainApp.models import Studies
from MainApp.models import Assignments
from MainApp.models import Tests

def course():
    return render_template('learning/learning_course_input.html')

def inputCourse(request):
    semester = None
    courseNumber = None
    courseName = None
    credits = None

    if request.method == 'POST':
        semester = request.form['semester']
        courseNumber = request.form['courseNumber']
        courseName = request.form['courseName']
        credits = request.form['credits']

        result = Courses.query.filter_by(CourseNumber=courseNumber).first()
        # Check the request and upload the database
        if result is None:
            tupleToInsert = Courses(semester, courseNumber, courseName, credits)
            db.session.add(tupleToInsert)
            db.session.commit()
            return '<h2>Successfully added.</h2>'
        else:
            return '<h2>Course already existed!!!</h2>'

def listAllCourses():
    '''
    result = db.session.execute('SELECT * FROM Courses')
    return render_template('learning_courses_listAll.html', courses=result)
    '''
    return render_template('learning/learning_courses_listAll.html', courses=Courses.query.all())

def study():
    returnedTuples = Courses.query.with_entities(Courses.CourseNumber)
    courseNumbers = [r.CourseNumber for r in returnedTuples]
    return render_template('learning/learning_study_input.html', courseNumbers=courseNumbers)

def inputStudy(request):
    courseNumber = None
    date = None
    duration = None
    content = None

    if request.method == 'POST':
        courseNumber = request.form['courseNumber']
        date = request.form['date']
        duration = request.form['duration']
        content = request.form['content']

        # tupleToInsert = Studies(courseNumber, date, duration, content)
        # db.session.add(tupleToInsert)
        # db.session.commit()
        result = Courses.query.filter_by(CourseNumber=courseNumber).first()
        db.session.delete(result)
        db.session.commit()
        return '<h2>Successfully added.</h2>'
