from flask import Flask                  #Flask
from flask import render_template        #rendering template
from flask_sqlalchemy import SQLAlchemy  #SQL
from MainApp.database import db          #created database
from MainApp.models import Courses       #include the table in database

def course():
    return render_template('learning_course_input.html')

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
    return render_template('learning_list_courses.html', values=Courses.query.all())
